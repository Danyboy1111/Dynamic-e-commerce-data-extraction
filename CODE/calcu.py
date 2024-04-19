import os
import numpy as np
import pytesseract
from PIL import Image
import random
import pandas as pd
from ultralytics import YOLO
import numpy as np
import cv2

def extract_text_from_image(image_path):
    try:
        # Open the image file
        with Image.open(image_path) as img:
            # Use pytesseract to extract text
            text = pytesseract.image_to_string(img)
            return text
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def process_image_folder(folder_path):
    data = {}
    a = []
    f_p = os.path.join(folder_path, 'image.jpg')
    if os.path.exists(f_p):
        a.append(f_p)
    f_p2 = os.path.join(folder_path, 'pdetails.jpg')
    if os.path.exists(f_p2):
        e_text = extract_text_from_image(f_p2).replace(' ', '')
        e_text = e_text.replace('\n', '')
        e_text = e_text.replace('\x0c', '')
        a.append(e_text)
    a.append(random.randint(300, 5000))
    f_p3 = os.path.join(folder_path, 'discount.jpg')
    if os.path.exists(f_p3):
        a.append("best Deal")
    else:
        a.append("regular`")
    f_p4 = os.path.join(folder_path, '4star.jpg')
    f_p5 = os.path.join(folder_path, '5star.jpg')
    f_p6 = os.path.join(folder_path, '2.5star.jpg')
    if os.path.exists(f_p4):
        a.append("4star")
    elif os.path.exists(f_p5):
        a.append("5star")
    elif os.path.exists(f_p6):
        a.append("2.5star")
              
    # Iterate over each image file
    for image_file in os.listdir(folder_path):
        # Construct the full path to the image file
        image_path = os.path.join(folder_path, image_file)
    
        # Open the image file using PIL (Python Imaging Library)
        with Image.open(image_path) as img:
            # Use Tesseract to extract text from the image
            extracted_text = pytesseract.image_to_string(img)
    
        if ('% off)' in extracted_text):
            extracted_text = extracted_text.replace('\n', '')
            extracted_text = extracted_text.replace('\x0c', '')
            a.append(extracted_text)
            print("herooooooo")
        if ('s, get ' in extracted_text):
            extracted_text = extracted_text.replace('\n', '')
            extracted_text = extracted_text.replace('\x0c', '')
            a.append(extracted_text)
            print("mherooooooooo")
        
    return a

def func2():
    # Initialize YOLO model
    model = YOLO('/home/dinesh/Documents/MajorPro/best_details.pt')

    # Input and output folders
    input_folder = '/home/dinesh/Documents/MajorPro/Products'
    output_folder = '/home/dinesh/Documents/MajorPro/Details'

    # Object names
    names = ['dog', 'person', 'cat', 'tv', 'car', 'meatballs', 'marinara sauce', 'tomato soup', 'chicken noodle soup',
             'french onion soup', 'chicken breast', 'ribs', 'pulled pork', 'hamburger', 'cavity', 'image', 'pdetails',
             '3.5star', 'price', 'discount', 'delivery', '5star', 'reviews', '4star', 'bestdeal', '2.5star', 'offer',
             '4.5star', '4.5', '3star']

    # Iterate over each image in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            # Load the image
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)

            # Apply YOLO model
            results = model(image)

            # Create a folder for each image
            image_folder_name = os.path.splitext(filename)[0]
            image_folder_path = os.path.join(output_folder, image_folder_name)
            os.makedirs(image_folder_path, exist_ok=True)

            # Iterate over each detected object
            for idx, r in enumerate(results):
                # Get the bounding box coordinates for all detected objects
                boxes_array = r.boxes.xyxy.cpu().numpy()

                # Get confidence scores and class labels
                confidence_array = r.boxes.conf.cpu().numpy()
                class_array = r.boxes.cls.cpu().numpy()

                # Combine x, y, w, h, confidence, class into a single array for each object
                combined_array = np.column_stack((boxes_array, confidence_array, class_array))

                # Iterate over each detected object
                for i, box_info in enumerate(combined_array):
                    x_min, y_min, x_max, y_max, confidence, class_id = box_info

                    # Get the object name using the class ID
                    object_name = names[int(class_id)]

                    # Crop the object from the original image
                    identified_object = image[int(y_min):int(y_max), int(x_min):int(x_max)]

                    # Save the cropped object to the image folder using the object name as the file name
                    output_filename = f'{object_name}_{idx + 1}_{i + 1}.jpg'
                    output_path = os.path.join(image_folder_path, output_filename)
                    cv2.imwrite(output_path, identified_object)
                    print(f"Object {idx + 1}_{i + 1} in {filename} saved as: {output_path}")

            print(f"Objects detected in {filename} saved in folder: {image_folder_path}")

# Call the function




def func1():
    # Initialize YOLO model
    model = YOLO('/home/dinesh/Documents/MajorPro/best_product.pt')

    # Input and output folders
    input_folder = '/home/dinesh/Documents/wwde-20240217T125839Z-001/Images/'
    output_folder = '/home/dinesh/Documents/MajorPro/Products'

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over each image in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            # Load the image
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)
            
            # Apply YOLO model
            results = model(image)
            
            # Check if any objects were detected
            if any(len(r) > 0 for r in results):
                # Iterate over each detected object
                for idx, r in enumerate(results):
                    # Get the bounding box coordinates for all detected objects
                    boxes_array = r.boxes.xyxy.cpu().numpy()

                    # Iterate over each detected object
                    for i, box_info in enumerate(boxes_array):
                        x_min, y_min, x_max, y_max = box_info

                        # Crop the object from the original image
                        identified_object = image[int(y_min):int(y_max), int(x_min):int(x_max)]

                        # Generate a unique filename for the object
                        output_filename = f'{filename}_object_{idx + 1}_{i + 1}.jpg'
                        output_path = os.path.join(output_folder, output_filename)
                        cv2.imwrite(output_path, identified_object)
                        print(f"Object {idx + 1}_{i + 1} in {filename} saved as: {output_path}")

                print(f"Objects detected in {filename}")
            else:
                print(f"No objects detected in {filename}")

# Call the func_s
def main():
    func1()
    func2()
    mata=[]
    # Specify the parent folder containing subfolders with images
    parent_folder = "/home/dinesh/Documents/MajorPro/Details"

    # Check if the specified path exists and is a folder
    if not os.path.exists(parent_folder):
        print("Parent folder path does not exist.")
        return
    if not os.path.isdir(parent_folder):
        print("Specified path is not a folder.")
        return

    # Get a list of subfolders in the parent folder
    subfolders = [folder for folder in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, folder))]

    # Iterate over each subfolder
    for subfolder in subfolders:
        folder_path = os.path.join(parent_folder, subfolder)
        print(f"Processing folder: {folder_path}")

        # Process the folder and get the data
        data = process_image_folder(folder_path)
        mata.append(data)
    print("finally the answer is ")
    print("finally the answer is ")
    print("finally the answer is ")
    print("finally the answer is ")
    print("finally the answer is ")
     
    print(mata)
    df = pd.DataFrame(mata)

    print("finally the answer is ")
    print("finally the answer is ")
    print(df)
    excel_file_path = "/home/dinesh/Documents/MajorPro/output.xlsx"
    df.to_excel(excel_file_path, index=False)

    #print(df)

if __name__ == "__main__":
    main()
