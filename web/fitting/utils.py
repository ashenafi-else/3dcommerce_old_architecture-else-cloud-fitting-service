from datetime import datetime
import os

attachment_path = {
	'Last': lambda instance, filename: os.path.sep.join(
			[
				instance.__class__.__name__,
				instance.product.uuid,
				str(instance.size),
				filename
			]
		),
	'Scan': lambda instance, filename: os.path.sep.join(
			[
				instance.__class__.__name__,
				instance.user.uuid,
				'{}-{}-{}'.format(datetime.now().year, datetime.now().month, datetime.now().day),
				filename
			]
		),
	'ProductProxy': lambda instance, filename: os.path.sep.join(
			[
				instance.__class__.__name__,
				instance.uuid,
				'{}-{}-{}'.format(datetime.now().year, datetime.now().month, datetime.now().day),
				filename
			]
		),
}


def gen_file_name(instance, filename):
	return attachment_path[instance.__class__.__name__](instance, filename)