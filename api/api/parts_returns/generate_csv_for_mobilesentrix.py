import csv

def generate_parts_obj(input_csv_file):
    with open(input_csv_file) as csv_file:
        next(csv_file)
        csv_reader = csv.reader(csv_file, delimiter=',')
        parts_obj = {}
        last_sku_used = ''
        for line in csv_reader:
            if line[1]:
                parts_obj[f"{line[1]}"] = {}
                parts_obj[f"{line[1]}"]['name'] = line[1]
                parts_obj[f"{line[1]}"]["quantity"] = 1
                last_sku_used = f"{line[1]}"
            if not line[1]:
                if line[5]:
                    parts_obj[f"{last_sku_used}"]["quantity"] += int(line[5])
    csv_file.close()
    return parts_obj

def generate_output_csv(output_csv_file, parts_obj):
    with open(output_csv_file, 'w') as output_csv_file:
        fieldnames = ["SKU", "QTY"]

        csv_writer = csv.DictWriter(output_csv_file, fieldnames=fieldnames)

        csv_writer.writeheader()
        for obj in parts_obj:
            csv_writer.writerow({'SKU': parts_obj[obj]["name"], 'QTY': parts_obj[obj]["quantity"]})


def generate_csv_for_mobilesentrix(input_csv_file, output_csv_file):
    parts_obj = generate_parts_obj(input_csv_file)
    generate_output_csv(output_csv_file, parts_obj)