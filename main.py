import csv
import re


def get_correct_name_list(data):
    full_name = " ".join(data).strip().split()
    if len(full_name) < 3:
        full_name += ['']
    return full_name


def get_correct_phone(data):
    pattern = r"(8|\+7)?[\s(]*(\d{3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})*[\sа-я.()]*(\d*)[)]*"
    subst_pattern1 = r"+7(\2)\3\4\5"
    subst_pattern2 = r"+7(\2)\3\4\5 доб. \6"
    phone = str()
    res = re.search(pattern, data)
    if isinstance(res, re.Match):
        if res.group(6):
            phone = re.sub(pattern, subst_pattern2, data)
        else:
            phone = re.sub(pattern, subst_pattern1, data)
    return phone


def get_data_dict(lst, headers):
    result = get_correct_name_list(lst[:3]) + lst[3:5] + [get_correct_phone(lst[-2])] + [lst[-1]]
    dct = {key: value for key, value in zip(headers, result)}
    return dct


def update_contacts(data):
    headers = data[0]
    cont_list = list()
    del_index = list()
    for index, lst1 in enumerate(data[1:], start=1):
        dct1 = get_data_dict(lst1, headers)
        for lst2 in data[index + 1:]:
            dct2 = get_data_dict(lst2, headers)
            if dct2['lastname'] == dct1['lastname'] and dct2['firstname'] == dct1['firstname']:
                del_index.append(data.index(lst2))
                for key, value in dct2.items():
                    if value:
                        dct1[key] = value
        if index not in del_index:
            cont_list.append(dct1)
    return cont_list


with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

with open("phonebook.csv", "w") as f:
    datawriter = csv.DictWriter(f, fieldnames=contacts_list[0], delimiter=',')
    datawriter.writeheader()
    datawriter.writerows(update_contacts(contacts_list))
