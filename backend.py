from DataPrep import preprocess
import os

path = './Conversion_Charts/'
AllUnits = []
allowedOperators = ['*', '/', '(', ')', '**', '-', '+']

for txt in os.listdir(path):
    try:
        AllUnits.append(preprocess(os.path.join(path, txt)))
    except UnicodeDecodeError:
        pass
DerivedUnits = preprocess("./Derived_Units.txt")


def ConvertDerived(unit_in, unit_out, mag):
    global allowedOperators

    def ConvertMonomers(raw):
        global allowedOperators
        Monomers = []
        for item in raw:
            if item in allowedOperators:
                Monomers.append(item)
            else:
                if item in [row[0] for row in DerivedUnits]:
                    baseUnit = [row[1] for row in DerivedUnits if row[0] == item][0]
                    Monomers.append("(")
                    Monomers.extend(baseUnit.split('_'))
                    Monomers.append(")")
                else:
                    Monomers.append(item)
        return Monomers

    def extractMonomers(raw):
        global allowedOperators
        Monomers = []
        for item in [items for items in raw if not (items in allowedOperators) and not items.lstrip("-+").isdigit()]:
            Monomers.append(item)
        return Monomers

    '''start'''
    user_in = unit_in
    raw_in = user_in.split('_')
    if not set(raw_in).isdisjoint([row[0] for row in DerivedUnits]):
        raw_in = ConvertMonomers(raw_in)
    Monomers_in = extractMonomers(raw_in)

    user_out = unit_out
    raw_out = user_out.split('_')
    if not set(raw_out).isdisjoint([row[0] for row in DerivedUnits]):
        raw_out = ConvertMonomers(raw_out)
    Monomers_out = extractMonomers(raw_out)

    Monomers_in_compare = []
    Monomers_out_compare = []
    Expression_in = ''
    Expression_out = ''

    for i in range(0, len(Monomers_in)):
        Monomer_compare = Convert(f"1;{Monomers_in[i]}", "toBase")
        Monomers_in_compare.append(Monomer_compare)

    for item in raw_in:
        if item not in allowedOperators and not item.lstrip("-+").isdigit():
            item_substitute = Monomers_in_compare[0]
            Monomers_in_compare.pop(0)
        else:
            item_substitute = item
        Expression_in = Expression_in + str(item_substitute)

    for i in range(0, len(Monomers_out)):
        Monomer_compare = Convert(f"1;{Monomers_out[i]}", "toBase")
        Monomers_out_compare.append(Monomer_compare)

    for item in raw_out:
        if item not in allowedOperators and not item.lstrip("-+").isdigit():
            item_substitute = Monomers_out_compare[0]
            Monomers_out_compare.pop(0)
        else:
            item_substitute = item
        Expression_out = Expression_out + str(item_substitute)
    return float(mag) * eval(Expression_in) / eval(Expression_out)


def Convert(ans, unit):
    mag = ans.split(";")[0].strip()
    unit_in = ans.split(";")[1]
    unit_in_multiple = 0
    unit_in_valid = []

    unit_out = str(unit)
    unit_out_multiple = 0
    unit_out_valid = []
    for units in AllUnits:
        for unit in units:
            if unit_in.strip() == unit[0].strip():
                unit_in_multiple = unit[1]
                unit_in_valid = units
            if unit_out.strip() == unit[0].strip():
                unit_out_multiple = unit[1]
                unit_out_valid = units

    if unit_out == "toBase":
        return float(mag) * float(unit_in_multiple)
    elif unit_in_multiple is 0 or unit_out_multiple is 0:
        # Not Base Unit:
        return ConvertDerived(unit_in, unit_out, mag)
    elif unit_in_valid != unit_out_valid:
        # Can't convert error
        return "How is this possible?"
    else:
        answer = float(mag) * float(unit_in_multiple) / float(unit_out_multiple)
        return answer


while True:
    print("The use of this program requires strict formatting of inputs due to a lack of GUI. \n"
          "An acceptable input must look like this: \n"
          "magnitude;(_unit1_+_unit2_)_*_unit3")
    INPUT = input("Please input the input unit, separating its magnitude and unit with a semi-colon: ';'")
    OUTPUT = input("What is your desired output unit?")
    print(Convert(INPUT, OUTPUT))
