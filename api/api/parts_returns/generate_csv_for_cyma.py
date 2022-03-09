import csv

def generate_parts_obj(input_csv_file):
    with open(input_csv_file) as csv_file:
        next(csv_file)
        csv_reader = csv.reader(csv_file, delimiter=',')
        parts_obj = {}
        last_sku_used = ''
        for line in csv_reader:
            if line[4]:
                if line[4] not in parts_obj:
                    parts_obj[f"{line[4]}"] = {}
                    parts_obj[f"{line[4]}"]['name'] = line[4]
                    parts_obj[f"{line[4]}"]["quantity"] = int(line[5])
                    last_part_name_used = f"{line[4]}"
                else:
                    if line[5]:
                        parts_obj[f"{line[4]}"]["quantity"] += int(line[5])
    return parts_obj

def generate_output_csv(output_csv_file, parts_obj):
    with open(output_csv_file, 'w') as output_csv_file:
        fieldnames = ["part_number", "quantity"]

        csv_writer = csv.DictWriter(output_csv_file, fieldnames=fieldnames)

        csv_writer.writeheader()
        for obj in parts_obj:
            csv_writer.writerow({'part_number': parts_obj[obj]["name"], 'quantity': parts_obj[obj]["quantity"]})

def generate_csv_for_mobilesentrix(input_csv_file, output_csv_file):
    parts_obj = generate_parts_obj(input_csv_file)
    generate_output_csv(output_csv_file, parts_obj)