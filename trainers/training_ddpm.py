import random

import numpy as np
import torch
import torch.nn.functional as F

import PIL.Image
from accelerate import Accelerator
from datasets import load_dataset
from diffusers import DDPM, DDPMScheduler, UNetModel
from torchvision.transforms import CenterCrop, Compose, Lambda, RandomHorizontalFlip, Resize, ToTensor
from tqdm.auto import tqdm
from transformers import get_linear_schedule_with_warmup


def set_seed(seed):
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)


set_seed(0)

accelerator = Accelerator(mixed_precision="fp16")

model = UNetModel(ch=128, ch_mult=(1, 2, 4, 8), resolution=64)
noise_scheduler = DDPMScheduler(timesteps=1000)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

num_epochs = 100
batch_size = 8
gradient_accumulation_steps = 8

augmentations = Compose(
    [
        Resize(64),
        CenterCrop(64),
        RandomHorizontalFlip(),
        ToTensor(),
        Lambda(lambda x: x * 2 - 1),
    ]
)
dataset = load_dataset("huggan/pokemon", split="train")


def transforms(examples):
    images = [augmentations(image.convert("RGB")) for image in examples["image"]]
    return {"input": images}


dataset = dataset.shuffle(seed=0)
dataset.set_transform(transforms)
train_dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=False)

lr_scheduler = get_linear_schedule_with_warmup(
    optimizer=optimizer,
    num_warmup_steps=1000,
    num_training_steps=(len(train_dataloader) * num_epochs) // gradient_accumulation_steps,
)

model, optimizer, train_dataloader, lr_scheduler = accelerator.prepare(
    model, optimizer, train_dataloader, lr_scheduler
)

for epoch in range(num_epochs):
    model.train()
    pbar = tqdm(total=len(train_dataloader), unit="ba")
    pbar.set_description(f"Epoch {epoch}")
    for step, batch in enumerate(train_dataloader):
        clean_images = batch["input"]
        noisy_images = torch.empty_like(clean_images)
        bsz = clean_images.shape[0]

        timesteps = torch.randint(0, noise_scheduler.timesteps, (bsz,), device=clean_images.device).long()
        for idx in range(bsz):
            noise = torch.randn_like(clean_images[0]).to(clean_images.device)
            noisy_images[idx] = noise_scheduler.forward_step(clean_images[idx], noise, timesteps[idx])

        if step % gradient_accumulation_steps == 0:
            with accelerator.no_sync(model):
                output = model(noisy_images, timesteps)
                loss = F.l1_loss(output, clean_images)
                accelerator.backward(loss)
        else:
            output = model(noisy_images, timesteps)
            loss = F.l1_loss(output, clean_images)
            accelerator.backward(loss)
            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad()
        pbar.update(1)
        pbar.set_postfix(loss=loss.detach().item(), lr=optimizer.param_groups[0]["lr"])

        optimizer.step()

    # eval
    model.eval()
    with torch.no_grad():
        pipeline = DDPM(unet=model, noise_scheduler=noise_scheduler)
        generator = torch.Generator()
        generator = generator.manual_seed(0)
        # run pipeline in inference (sample random noise and denoise)
        image = pipeline(generator=generator)

        # process image to PIL
        image_processed = image.cpu().permute(0, 2, 3, 1)
        image_processed = (image_processed + 1.0) * 127.5
        image_processed = image_processed.type(torch.uint8).numpy()
        image_pil = PIL.Image.fromarray(image_processed[0])

        # save image
        pipeline.save_pretrained("./poke-ddpm")
        image_pil.save(f"./poke-ddpm/test_{epoch}.png")
