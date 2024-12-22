# Phishing Webpage Detection System Using Multimodal Deep Learning Model

## About The Project

The phishing webpage detection system comprises three components: an API server, a verification website and a browser extension. This system aids in identifying phishing webpages by analyzing features from URLs and HTML DOM structures. The model is trained using data collected from [PhishTank](https://phishtank.org/) (phishing URLs) and [Tranco](https://tranco-list.eu/) (legitimate URLs)

## Folder Structure

Corresponding to the three components of the system, the directory structure is divided into three main folders: `app`, `website` and `extension`:

- `app`: This directory contains all elements related to building and training the model, and from that model, developing an API to return the likelihood of a website being phishing based on the input URL.

- `website`: This folder includes a React application used to create the phishing website verification site.

- `extension`: This directory holds the necessary components to develop a phishing detection extension for Chromium-based browsers.

## Built With

- Google Colab Pro
- TensorFlow
- FastAPI
- Node.js
- React
- Chrome Extension

## Getting Started

To start the project, you need to install the necessary software and follow the steps below.

### Prerequisites

- To rerun the notebook files, you need Google Colab Pro with GPU or TPU and at least 300GB of RAM.

- Anaconda (recommended) or a Python virtual environment is required to create an isolated environment for installing the necessary dependencies to run the API built from the trained model.

- Node.js version 22.11 or higher.

### Running the Application

#### API Server

**Build and train models**

The files used for building and training the model are located in the app/notebooks directory. These files include:

- collecting.ipynb: Collects HTML data from a list of URLs to create a comprehensive dataset.

- preprocessing.ipynb: Preprocesses the data and splits it into training, validation, and test sets, then saves them into an H5 file.

- training.ipynb: Contains the process and evaluation results of the best-trained model.

- training(2).ipynb: Includes the process and evaluation results of the model using 2 heads in the Transformer Encoder.

- training(8).ipynb: Includes the process and evaluation results of the model using 8 heads in the Transformer Encoder.

- training_separated.ipynb: Contains the process and evaluation results of two models: one using only URLs and the other using only HTML.

- training_separated(LSTM+GRU).ipynb: Contains the process and evaluation results of two models utilizing LSTM and GRU instead of the Transformer Encoder.

- training_experiment.ipynb: Contains experiments with varying model parameters.

To rerun these files, open them in Colab with a TPU or GPU and sufficient RAM. These notebooks utilize data and certain functions from the project directory stored on Google Drive. Therefore, follow these steps:

1. Mount Google Drive

```python
    from google.colab import drive
    drive.mount('/content/drive')
```

2. Navigate to the Project Directory

Comment out the following code in the notebook, as it's only used to update changes of the utilized functions from local to Drive via GitHub:

```python
    %cd /content/drive/MyDrive/Github
    %cd Phishing-Website-Detection/app
    !git config --global user.email 'nguyenphong10042002@gmail.com'
    !git config --global user.name 'Akechi1412'
    !git fetch origin
    !git reset --hard origin/main
```

If you already have the project directory in your Google Drive, navigate to the app folder of the project.

If the project directory is not yet in your Drive, you can use the following code to clone the project directory into your Drive and then navigate to the app folder:

```python
    !git clone https://github.com/Akechi1412/Phishing-Website-Detection.git
```

The code provided should be executed only once when the project directory is not yet present in your Google Drive.

**Run the API application**

1. Setup Python environment

Set up the Python environment using Anaconda or a Python virtual environment. In cases where a pre-trained model is available in the `app/models directory`, use Python version 3.10.12. Otherwise, use a Python version compatible with the trained model.

2. Install dependencies

Ensure that the project directory has been cloned to your computer. If training a new model, adjust the TensorFlow version in the `app/requirements.txt` file to match the TensorFlow version used for the model.

Navigate to the `app` directory of the project in the terminal. Run the following command to install the necessary dependencies into the configured Python environment:

```sh
    pip install -r requirements.txt
```

3. Start FastAPI application

Run the following command to start the FastAPI application:

```sh
    uvicorn app:app --reload
```

Open the docs page and test the API at [http://localhost:8000/docs](http://localhost:8000/docs).

#### Verification Website

1. Install dependenc

Ensure that Node.js with a compatible version is installed. Navigate to the `website` directory of the project in the terminal. Run the following command to install the necessary dependencies:

```sh
    npm install
```

2. Setup environment variables

Create a `.env.local` file in the `website` directory with the following content:

```sh
    PD_PHISHING_API_BASE=http://localhost:8000
    PD_SEVICE_ID=<YOUR_SEVICE_ID(optional)>
    PD_TEMPLATE_ID=<YOUR_TEMPLATE_ID(optional)>
    PD_PUBLIC_KEY=<YOUR_PUBLIC_KEY(optional)>
    PD_CAPCHA_SITE_KEY=<YOUR_CAPCHA_SITE_KEY(optional)>
    PD_CHROME_EXTENSION_URL=<YOUR_CHROME_EXTENSION_URL(optional)>
```

Here:

- `PD_PHISHING_API_BASE` is the URL of the API server started earlier.
- `PD_SERVICE_ID, PD_TEMPLATE_ID`, and PD_PUBLIC_KEY are for configuring EmailJS for the contact section; these can be omitted if not needed.

- `PD_CAPTCHA_SITE_KEY` is for setting up reCAPTCHA to prevent spam on the website; this can also be omitted if not needed.
- `PD_CHROME_EXTENSION_URL` points to the system's extension page on the Chrome Web Store and can be omitted if unnecessary.

3. Start React application

Ensure the API server is running at this point. Run the following command to start the React application for the website:

```sh
    npm run dev
```

Open http://localhost:5173 in your browser and verify that the website is functioning correctly.

#### Browser Extension

This browser extension is compatible with Chrome and other Chromium-based browsers such as Opera Browser or Brave. The instructions below are specific to Chrome, but the setup for other browsers is similar.

First, open `chrome://extensions` in the Chrome browser, then enable Developer mode in the upper-right corner. Once enabled, the "Load unpacked" option will appear in the top-left corner. Click it to upload the extension directory of the project. At this point, the extension can be used like any other extension, but in developer mode, meaning code changes made locally will be instantly updated in the browser.
