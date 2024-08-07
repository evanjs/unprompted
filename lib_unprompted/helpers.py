# Contains helper methods that do not rely on Unprompted class data
# nor are they exclusively useful for said class

pil_resampling_dict = {}
pil_resampling_dict["Nearest Neighbor"] = 0
pil_resampling_dict["Box"] = 4
pil_resampling_dict["Bilinear"] = 2
pil_resampling_dict["Hamming"] = 5
pil_resampling_dict["Bicubic"] = 3
pil_resampling_dict["Lanczos"] = 1


def strip_str(string, chop):
	"""Removes substring `chop` from the beginning or end of given `string`"""
	while True:
		if chop and string.endswith(chop):
			string = string[:-len(chop)]
		else:
			break
	while True:
		if chop and string.startswith(chop):
			string = string[len(chop):]
		else:
			break
	return string


def sigmoid(x):
	import math
	return 1 / (1 + math.exp(-x))


def is_equal(var_a, var_b):
	"""Checks if two variables equal each other, taking care to account for datatypes."""
	if (is_float(var_a)):
		var_a = float(var_a)
	if (is_float(var_b)):
		var_b = float(var_b)
	if (str(var_a) == str(var_b)):
		return True
	else:
		return False


def is_not_equal(var_a, var_b):
	"""Checks if two variables do not equal each other, taking care to account for datatypes."""
	return not is_equal(var_a, var_b)


def is_float(value):
	"""Tests whether variable is a float by attempting to convert it to a float."""
	try:
		float(value)
		return True
	except:
		return False


def is_int(value):
	"""Tests whether variable is an integer by attempting to convert it to an integer."""
	try:
		int(value)
		return True
	except:
		return False


def ensure(var, datatype):
	"""Ensures that a variable is a given datatype"""
	if isinstance(var, datatype):
		return var
	else:
		if datatype == list:
			return [var]
		return datatype(var)


def autocast(var):
	"""Converts a variable between string, int, and float depending on how it's formatted"""
	original_var = var
	if original_var == "inf" or original_var == "-inf":
		return (original_var)
	elif (is_float(var)):
		var = float(var)
		if int(var) == var and "." not in str(original_var):
			var = int(var)
	elif (is_int(var)):
		var = int(var)
	return (var)


def pil_to_cv2(img):
	import cv2, numpy
	return cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)


def cv2_to_pil(img):
	import cv2
	from PIL import Image
	return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def tensor_to_pil(tensor):
	import numpy as np
	from PIL import Image

	# Move the tensor to CPU if it's not already
	tensor = tensor.cpu()

	# Remove the batch dimension if it exists
	if tensor.ndim == 4:
		tensor = tensor[0]

	# Convert the tensor to a numpy array
	array = tensor.numpy()

	# If the tensor is in the format (C, H, W), transpose it to (H, W, C)
	# if array.shape[0] == 3:
	# 	array = array.transpose(1, 2, 0)

	# Convert the numpy array to an image
	array = (array * 255).astype(np.uint8)
	image = Image.fromarray(array)

	return image


def pil_to_tensor(image):
	import numpy as np
	from PIL import Image
	import torch

	# Convert the PIL image to a numpy array
	array = np.array(image)

	# Normalize the numpy array to the range [0, 1]
	array = array.astype(np.float32) / 255.0

	# If the array is in the format (H, W, C), transpose it to (C, H, W)
	# if array.ndim == 3:
	# 	array = array.transpose(2, 0, 1)

	# Convert the numpy array to a tensor
	tensor = torch.from_numpy(array)

	# Add a batch dimension
	tensor = tensor.unsqueeze(0)

	return tensor


def str_to_rgb(color_string):
	"""Converts a color string to a tuple of RGB values"""
	if color_string[0].isdigit():
		return tuple(map(int, color_string.split(',')))
	elif color_string.startswith("#"):
		return bytes.fromhex(color_string[1:])


def str_to_pil(string):
	from PIL import Image
	log = get_logger()

	if isinstance(string, str) and string.startswith("<PIL.Image.Image"):
		# Get the PIL object from the memory address
		# <PIL.Image.Image image mode=RGBA size=1024x1024 at 0x...>

		try:
			import ctypes
			import re

			# Extract the memory address from the string
			address = re.search(r"at (0x[0-9A-F]+)", string).group(1)

			# Convert the memory address to an integer
			address = int(address, 16)

			# Create a ctypes pointer to the memory address.
			img = ctypes.cast(address, ctypes.py_object).value

			# Validate the object
			if not isinstance(img, Image.Image):
				log.error(f"Failed to extract PIL image from memory address: {address}, {string}, {type(img)}")
				return False

			log.debug(f"Successfully extracted PIL image from memory address: {img}")
			return img
		except:
			log.exception(f"Failed to extract PIL image from memory address: {string}")
			return False
	else:
		try:
			import glob, random, os
			files = glob.glob(string)
			if (len(files) == 0):
				log.error(f"No files found at this location: {string}")
				return ("")
			file = random.choice(files)

			log.debug(f"Loading file: {file}")

			if not os.path.exists(file):
				log.error(f"File does not exist: {file}")
				return False

			img = Image.open(string)
			return img
		except:
			log.exception(f"Failed to open image: {string}")
			return False


def get_logger(logger=None):
	if not logger:
		try:
			import logging
			logger = logging.getLogger("Unprompted")
		except:
			logger = print
	return logger


def download_file(filename, url, logger=None, overwrite=False, headers=None):
	import os, requests

	log = get_logger(logger)

	if overwrite or not os.path.exists(filename):
		# Make sure directory structure exists
		os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

		log.info(f"Downloading file into: {filename}...")
		response = requests.get(url, stream=True, headers=headers)
		if response.status_code != 200:
			log.error(f"Error when trying to download `{url}` to `{filename}`. Dtatus code received: {response.status_code}")
			return False
		try:
			with open(filename, 'wb') as fout:
				for block in response.iter_content(4096):
					fout.write(block)
		except:
			log.exception(f"Error when writing download to `{filename}`.")
			return False

	return True


def import_file(full_name, path):
	"""Allows importing of modules from full filepath, not sure why Python requires a helper function for this in 2023"""
	from importlib import util

	spec = util.spec_from_file_location(full_name, path)
	mod = util.module_from_spec(spec)

	spec.loader.exec_module(mod)
	return mod


def list_set(this_list, index, value, null_value=False):
	"""Helper function to set array indexes that are outside the array's current length"""
	while (len(this_list) <= index):
		this_list.append(null_value)
	this_list[index] = value


def str_with_ext(path, default_ext=".json"):
	import os
	if os.path.exists(path) or default_ext in path:
		return path
	return path + default_ext


def create_load_json(file_path, default_data={}, encoding="utf8"):
	import json
	try:
		# If the file already exists, load its content
		with open(file_path, "r", encoding=encoding) as file:
			data = json.load(file)
	# If the file doesn't exist, create it with default data
	except FileNotFoundError:
		with open(file_path, "w", encoding=encoding) as file:
			json.dump(default_data, file, indent=4)
		data = default_data

	return data


def unsharp_mask(image, amount=1.0, kernel_size=(5, 5), sigma=1.0, threshold=0):
	"""Return a sharpened version of the image, using an unsharp mask."""
	import numpy, cv2
	from PIL import Image
	image = numpy.array(image).astype(numpy.uint8)
	blurred = cv2.GaussianBlur(image, kernel_size, sigma)
	sharpened = float(amount + 1) * image - float(amount) * blurred
	sharpened = numpy.maximum(sharpened, numpy.zeros(sharpened.shape))
	sharpened = numpy.minimum(sharpened, 255 * numpy.ones(sharpened.shape))
	sharpened = sharpened.round().astype(numpy.uint8)
	if threshold > 0:
		low_contrast_mask = numpy.absolute(image - blurred) < threshold
		numpy.copyto(sharpened, image, where=low_contrast_mask)
	return Image.fromarray(sharpened)


# Helper class that converts kwargs to attribute notation
# Many libraries expect to be fed options with argparse,
# which is not so straightforward inside of an A1111 extension
class AttrDict(dict):

	def __init__(self, *args, **kwargs):
		super(AttrDict, self).__init__(*args, **kwargs)
		self.__dict__ = self
