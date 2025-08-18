import boto3
import io
import time
from PIL import Image

s3 = boto3.client('s3')

def thumbnail_generator(event, context):
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    response = s3.get_object(Bucket=source_bucket, Key=key)
    image_data = response['Body'].read()

    ext = key.lower().split('.')[-1]
    if ext not in ["jpg", "jpeg", "png"]:
        print(f"Formato no soportado: {ext}")
        return

    sizes = [(50, 50), (100, 100), (200, 200)]
    for width, height in sizes:
        resize_image(image_data, source_bucket, width, height)

def resize_image(image_data, bucket, width, height):
    image = Image.open(io.BytesIO(image_data))
    image = image.resize((width, height), Image.LANCZOS)

    buffer = io.BytesIO()
    # Detectar formato original
    format_original = image.format
    if format_original and format_original.upper() == "PNG":
        ext = "png"
        image.save(buffer, format="PNG")
        content_type = "image/png"
    else:
        ext = "jpg"
        image.save(buffer, format="JPEG")
        content_type = "image/jpeg"
    buffer.seek(0)

    new_key = f"resized-{width}x{height}-{int(time.time())}.{ext}"

    s3.put_object(
        Bucket=bucket,
        Key=new_key,
        Body=buffer,
        ContentType=content_type
    )

    print(f"Imagen {width}x{height} subida como {new_key}")

