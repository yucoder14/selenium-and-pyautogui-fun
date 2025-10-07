from PIL import Image
import os 
import argparse

def crop_image(image, aspect_ratio): 
    img = Image.open(image)
    old_width, old_height = img.size 

    # if width is wider 
    if old_width / old_height > aspect_ratio: 
        new_width = int(old_height * aspect_ratio)
        left = (old_width - new_width) / 2
        top = 0 
        right = (old_width + new_width) / 2
        bottom = old_height
    # if height is taller 
    else:
        new_height = int(old_width / aspect_ratio)
        left = 0
        top = (old_height - new_height) / 2
        right = old_width
        bottom = (old_height + new_height) / 2

    crop_box = (int(left), int(top), int(right), int(bottom))
    cropped_img = img.crop(crop_box)

    # Desired base width
    basewidth = 200

    # Calculate new height to maintain aspect ratio
    wpercent = (basewidth / float(cropped_img.size[0]))
    hsize = int((float(cropped_img.size[1]) * float(wpercent)))

    # Resize the image with a resampling filter for better quality
    resized_img = cropped_img.resize((basewidth, hsize), Image.LANCZOS)

    return (image.split("/")[-1], resized_img)

if __name__=="__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", required=True, type=str)
    parser.add_argument("-o", "--output_dir", required=True, type=str)
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir

    if not os.path.exists(input_dir): 
        print(f"Error: {input_dir} is not a valid path")
        exit(2)

    try:
        os.makedirs(output_dir, exist_ok=True)
        output_dir = os.path.abspath(output_dir)
        print(f"Directory '{output_dir}' created or already exists.")
    except OSError as e:
        print(f"Error creating directory: {e}")
        exit(3)

    input_dir = [os.path.join(os.path.abspath(input_dir), image) for image in os.listdir(input_dir)] 

    cropped_images = [crop_image(image, 4/5) for image in input_dir]

    for name, image in cropped_images: 
        image.save(os.path.join(output_dir, name))
