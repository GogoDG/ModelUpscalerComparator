import os
import tkinter as tk
from tkinter import filedialog
import cv2

from metrics_calculator import calculate_metrics
from upscaler import MODEL_PATHS, upscale_image_rgb, upscale_image_with_transparency


def browse_file():
    file_path = filedialog.askopenfilename()
    entry_path.delete(0, tk.END)
    entry_path.insert(tk.END, file_path)


def upscale_image():
    file_path = entry_path.get()
    directory = os.path.dirname(file_path)
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    selected_model1 = var_model1.get()
    selected_model2 = var_model2.get()
    scale_factor = var_scale_factor.get()
    is_transparent = var_transparent.get()
    model_path1 = MODEL_PATHS.get((selected_model1.lower(), scale_factor))
    model_path2 = MODEL_PATHS.get((selected_model2.lower(), scale_factor))

    # Check for image transparency, upscale and save image
    if not is_transparent:
        new_file_path1 = file_name + '_' + selected_model1 + '_' + str(scale_factor) + 'K.png'
        new_file_path2 = file_name + '_' + selected_model2 + '_' + str(scale_factor) + 'K.png'
        upscaled_image1 = upscale_image_rgb(file_path, model_path1, selected_model1, scale_factor)
        cv2.imwrite(os.path.join(directory, new_file_path1), upscaled_image1)
        upscaled_image2 = upscale_image_rgb(file_path, model_path2, selected_model2, scale_factor)
        cv2.imwrite(os.path.join(directory, new_file_path2), upscaled_image2)
        window.destroy()
        create_comparison_window(file_path, (directory + "/" + new_file_path1), (directory + "/" + new_file_path2))
    else:
        new_file_path1 = file_name + '_' + selected_model1 + '_' + str(scale_factor) + 'K_tr.png'
        new_file_path2 = file_name + '_' + selected_model2 + '_' + str(scale_factor) + 'K_tr.png'
        upscaled_with_transparency1 = upscale_image_with_transparency(file_path, model_path1, selected_model1, scale_factor)
        cv2.imwrite(os.path.join(directory, new_file_path1), upscaled_with_transparency1)
        upscaled_with_transparency2 = upscale_image_with_transparency(file_path, model_path2, selected_model2, scale_factor)
        cv2.imwrite(os.path.join(directory, new_file_path2), upscaled_with_transparency2)
        window.destroy()
        create_comparison_window(file_path, (directory + "/" + new_file_path1), (directory + "/" + new_file_path2))


def update_scale_factor_options():
    if var_model1.get() == "lapsrn" and var_model2.get() == "lapsrn":
        radio_8x.config(state=tk.NORMAL)
    else:
        radio_8x.config(state=tk.DISABLED)


def create_comparison_window(original_image, image1_path, image2_path):
    original_image = cv2.imread(original_image)
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    window1_name = "Upscaled Image 1"
    window2_name = "Upscaled Image 2"

    # Call the function to calculate the metrics
    ssim1, mse1, psnr1 = calculate_metrics(original_image, image1)
    ssim2, mse2, psnr2 = calculate_metrics(original_image, image2)

    # Create windows for modified images
    cv2.namedWindow(window1_name)
    cv2.namedWindow(window2_name)

    # Move and resize the windows
    cv2.moveWindow(window1_name, 0, 0)
    cv2.moveWindow(window2_name, image1.shape[1], 0)

    # Add labels with comparison results to the images
    cv2.putText(image1, f"Model: {var_model1.get()}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 5, cv2.LINE_AA)
    cv2.putText(image1, f"PSNR: {psnr1:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 5, cv2.LINE_AA)
    cv2.putText(image1, f"MSE: {mse1:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 5, cv2.LINE_AA)
    cv2.putText(image1, f"SSIM: {ssim1:.4f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 5, cv2.LINE_AA)

    cv2.putText(image1, f"Model: {var_model1.get()}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(image1, f"PSNR: {psnr1:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(image1, f"MSE: {mse1:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(image1, f"SSIM: {ssim1:.4f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.putText(image2, f"Model: {var_model2.get()}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 5, cv2.LINE_AA)
    cv2.putText(image2, f"PSNR: {psnr2:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 5, cv2.LINE_AA)
    cv2.putText(image2, f"MSE: {mse2:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 5, cv2.LINE_AA)
    cv2.putText(image2, f"SSIM: {ssim2:.4f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 5, cv2.LINE_AA)

    cv2.putText(image2, f"Model: {var_model2.get()}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(image2, f"PSNR: {psnr2:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(image2, f"MSE: {mse2:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(image2, f"SSIM: {ssim2:.4f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Display the modified images
    cv2.imshow(window1_name, image1)
    cv2.imshow(window2_name, image2)

    # Wait for any key to close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Create the main window
window = tk.Tk()
window.title("Image Upscaler")
width = 500  # width in pixels
height = 300  # height in pixels
window.geometry(f"{width}x{height}")

# Create the components
label_path = tk.Label(window, text="File Path:")
entry_path = tk.Entry(window)
button_browse = tk.Button(window, text="Browse", command=browse_file)

label_model1 = tk.Label(window, text="Select Model 1:")
var_model1 = tk.StringVar(value="edsr")  # Set default position to "edsr"
radio_edsr1 = tk.Radiobutton(window, text="edsr", variable=var_model1, value="edsr",
                             command=update_scale_factor_options)
radio_espcn1 = tk.Radiobutton(window, text="espcn", variable=var_model1, value="espcn",
                              command=update_scale_factor_options)
radio_fsrcnn1 = tk.Radiobutton(window, text="fsrcnn", variable=var_model1, value="fsrcnn",
                               command=update_scale_factor_options)
radio_lapsrn1 = tk.Radiobutton(window, text="lapsrn", variable=var_model1, value="lapsrn",
                               command=update_scale_factor_options)

label_model2 = tk.Label(window, text="Select Model 2:")
var_model2 = tk.StringVar(value="edsr")  # Set default position to "edsr"
radio_edsr2 = tk.Radiobutton(window, text="edsr", variable=var_model2, value="edsr",
                             command=update_scale_factor_options)
radio_espcn2 = tk.Radiobutton(window, text="espcn", variable=var_model2, value="espcn",
                              command=update_scale_factor_options)
radio_fsrcnn2 = tk.Radiobutton(window, text="fsrcnn", variable=var_model2, value="fsrcnn",
                               command=update_scale_factor_options)
radio_lapsrn2 = tk.Radiobutton(window, text="lapsrn", variable=var_model2, value="lapsrn",
                               command=update_scale_factor_options)

label_scale_factor = tk.Label(window, text="Scale Factor:")
var_scale_factor = tk.IntVar(value=2)  # Set default position to 2
radio_2x = tk.Radiobutton(window, text="2", variable=var_scale_factor, value=2)
radio_4x = tk.Radiobutton(window, text="4", variable=var_scale_factor, value=4)
radio_8x = tk.Radiobutton(window, text="8", variable=var_scale_factor, value=8, state=tk.DISABLED)

var_transparent = tk.BooleanVar()
check_transparent = tk.Checkbutton(window, text="Is Transparent?", variable=var_transparent)

button_upscale = tk.Button(window, text="Upscale", command=upscale_image)

# Arrange the components using grid layout
label_path.grid(row=0, column=2, sticky=tk.E)
entry_path.grid(row=0, column=3, padx=5, pady=5)
button_browse.grid(row=0, column=4, padx=5, pady=5)

label_model1.grid(row=1, column=0, sticky=tk.E)
radio_edsr1.grid(row=1, column=2, sticky=tk.W)
radio_espcn1.grid(row=1, column=3, sticky=tk.W)
radio_fsrcnn1.grid(row=1, column=4, sticky=tk.W)
radio_lapsrn1.grid(row=1, column=5, sticky=tk.W)

label_model2.grid(row=2, column=0, sticky=tk.E)
radio_edsr2.grid(row=2, column=2, sticky=tk.W)
radio_espcn2.grid(row=2, column=3, sticky=tk.W)
radio_fsrcnn2.grid(row=2, column=4, sticky=tk.W)
radio_lapsrn2.grid(row=2, column=5, sticky=tk.W)

label_scale_factor.grid(row=3, column=0, sticky=tk.E)
radio_2x.grid(row=3, column=2, sticky=tk.W)
radio_4x.grid(row=3, column=3, sticky=tk.W)
radio_8x.grid(row=3, column=4, sticky=tk.W)

check_transparent.grid(row=4, column=0, columnspan=2, sticky=tk.W)

button_upscale.grid(row=5, column=2, columnspan=5, padx=5, pady=10)

# Run the main event loop
window.mainloop()
