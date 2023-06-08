import os

def get_dirs():
	base_dir = os.getcwd()
	src_dir = os.path.join(base_dir, "src")
	model_dir = os.path.join(src_dir, "model")
	data_dir = os.path.join(src_dir, "data")
	test_dir = os.path.join(src_dir, "test")
	template_dir = os.path.join(src_dir, "templates")

	dirs = {"base": base_dir,
	 "src": src_dir,
	 "model": model_dir,
	 "data": data_dir,
	 "test": test_dir,
	 "template": template_dir}

	return dirs