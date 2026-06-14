import subprocess

topic = "Defect_Recognition"
articles = [
    {
        "title": "Train YOLO for Object Detection on a Custom Dataset using Python",
        "link": "https://towardsdatascience.com/train-yolo-for-object-detection-on-a-custom-dataset-using-python-e4fe5eb94673/",
        "summary": "YOLO expects to find certain files and folders set up correctly in order to do the training on your custom dataset. First, you will need to open the file in the darknet/data/obj.names path where you put write your labels."
    },
    {
        "title": "How to Create a Simple Object Detection System with Python and ImageAI",
        "link": "https://towardsdatascience.com/how-to-create-a-simple-object-detection-system-with-python-and-imageai-ee1bcaf6b111/",
        "summary": "As you have seen, ImageAI library enables us to build an object detection system without having to deal with the complexity behind object detection model like ResNet or YOLO for custom objects."
    },
    {
        "title": "Intro to Autoencoders | TensorFlow Core",
        "link": "https://www.tensorflow.org/tutorials/generative/autoencoder",
        "summary": "This tutorial introduces autoencoders with three examples: the basics, image denoising, and anomaly detection. Autoencoder anomaly detection code implementation."
    },
    {
        "title": "Classifying objects from 3D CAD files - OpenCV Forum",
        "link": "https://forum.opencv.org/t/classifying-objects-from-3d-cad-files/8849",
        "summary": "Industrial inspection talks about “Machine Vision”. OpenCV industrial inspection."
    },
    {
        "title": "You Can’t Scale AI With Real Data Alone: A Practical Guide to Synthetic Data Generation | HackerNoon",
        "link": "https://hackernoon.com/you-cant-scale-ai-with-real-data-alone-a-practical-guide-to-synthetic-data-generation",
        "summary": "Synthetic data is transforming AI by solving privacy, bias, and scalability challenges. Learn methods, use cases, and key risks for Synthetic data generation for defects."
    }
]

# We don't want to re-add existing ones if they're exactly correct.
# Wait, actually, the file currently HAS all 5 of these!
