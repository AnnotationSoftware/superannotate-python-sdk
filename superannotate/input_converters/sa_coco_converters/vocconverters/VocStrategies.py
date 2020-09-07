class ObjectDetectionStrategy(VocConverter):
    name = "ObjectDetection converter"

    def __init__(
        self, dataset_name, export_root, project_type, output_dir, task,
        direction
    ):
        self.direction = direction
        super().__init__(
            dataset_name, export_root, project_type, output_dir, task
        )

        self.__setup_conversion_algorithm()

    def __setup_conversion_algorithm(self):
    	if self.direction == "to":
    		raise NotImplementedError("Doesn't support yet")
    	else:
    		if self.project_type == "vector":
    			if self.task == "object_detection":
    				self.conversion_algorithm = voc_object_detection_to_sa_vector
    			elif self.task == "instance_segmentation":
    				raise NotImplementedError("Doesn't support yet")

    def __str__(self):
    	return '{} object'.format(self.name)

    def from_sa_format(self):
    	pass

    def to_sa_format(self):
    	pass





