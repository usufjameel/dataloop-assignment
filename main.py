import time

import dtlpy as dl

project_name = "IndividualProject"
dataset_name = "AlgoImagePool"

dl.login()  # use browser login to create the bot

try:
    project = dl.projects.get(project_name=project_name)
except:
    project = dl.projects.create(project_name=project_name)

print("2.a Create a dataset (if existing, get it")
try:
    dataset = project.datasets.get(dataset_name=dataset_name)
except:
    project.datasets.create(dataset_name=dataset_name)
    dataset = project.datasets.get(dataset_name=dataset_name)

print("2.b Add three labels to the dataset recipe (class1, class2, and key)")

labels = [{"label_name": "class1"}, {"label_name": "class2"}, {"label_name": "key"}]
dataset.add_labels(label_list=labels)

print("2.c. upload directory with five images (Single upload to all items in the directory)")
print(
    "2.d Add a UTM metadata to an item user metadata - collection time {“collected”:<the current time in UTM timestamp>}")
metadata = dict()
metadata["user"] = dict()
metadata["user"]["collected"] = time.time()
dataset.items.upload(local_path="assets", item_metadata=metadata)

pages = dataset.items.list()

print("2.e Add a classification of class1 to the first two of the images you uploaded.")
print("2.f. Add a classification of class2 to the rest of the images you uploaded.")
print("2.g. Add five random key points with the label “key” to one item.")
for page in pages:
    for index, item in enumerate(page):
        builder = item.annotations.builder()
        if index == 0:
            builder.add(annotation_definition=dl.Point(x=10, y=10, label='key'))
            builder.add(annotation_definition=dl.Point(x=25, y=15, label='key'))
            builder.add(annotation_definition=dl.Point(x=70, y=45, label='key'))
            builder.add(annotation_definition=dl.Point(x=15, y=80, label='key'))
            builder.add(annotation_definition=dl.Point(x=90, y=101, label='key'))
        if index < 2:
            builder.add(annotation_definition=dl.Classification(label='class1'))
        else:
            builder.add(annotation_definition=dl.Classification(label='class2'))
        item.annotations.upload(builder)

print(
    "3. Create a query that selects only image items that have been labeled as “class1 and print the item name and item id of each item")

queryOneFilter = dl.Filters()
queryOneFilter.add_join(field='label', values='class1')

queryOnePages = dataset.items.list(queryOneFilter)

for itemPage in queryOnePages:
    for item in itemPage:
        print("\nItem Name:" + item.name)
        print("Item ID:" + item.id)

print(
    "4. Create a query that retrieves all point annotations from the dataset and prints the item name and item id of each item, and for each item, print for each annotation the annotation id, annotation label, and position of the point (x,y)")
queryTwoFilter = dl.Filters(resource=dl.FiltersResource.ANNOTATION)
queryTwoFilter.add(field="type", values="point")

queryTwoPages = dataset.items.list(queryTwoFilter)

print(queryTwoPages)

for page in queryTwoPages:
    for annotation in page:
        print("\nItem Name:" + annotation.item.name)
        print("Item ID:" + annotation.item.id)
        print("Annotation ID:" + annotation.id)
        print("Annotation Label:" + annotation.label)
        print("Annotation position: " + str(annotation.coordinates))
