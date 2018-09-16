import os
import sys
import shutil as su
import subprocess as subproc

programs = []
split_dict = {'Orphan':0}
program_dir = os.path.curdir
path = ''

if(len(sys.argv) < 2):
    path = os.path.curdir
else:
    path = sys.argv[1]
try:
    programs = os.listdir(path)
    os.mkdir(path + '\\Orphan')
    os.mkdir(path + '\\Metadata')

    for program in programs:
        if str(program).find('.py'):
            subparts = str(program).split('_')
            if len(subparts) > 1:
                try:
                    lab_id = int(subparts[-2])
                    try:
                        if lab_id < 236 and lab_id > 200:
                            split_dict[lab_id] = split_dict[lab_id] + 1
                            su.move(path + '\\' + program, path + '\\' + str(lab_id))
                            splitted_program_name = program.split('_')
                            os.rename(path + '\\' + str(lab_id) + '\\' + program, path + '\\' + str(lab_id) + '\\' + (str(program).replace(' ', '_')))
                        else:
                            split_dict['Orphan'] = split_dict['Orphan'] + 1
                            su.move(path + '\\' + program, path + '\\Orphan')
                    except KeyError as ke:
                        split_dict[lab_id] = 1
                        os.mkdir(path + '\\' + str(lab_id))
                        su.move(path + '\\' + program, path + '\\' + str(lab_id))
                        os.rename(path + '\\' + str(lab_id) + '\\' + program, path + '\\' + str(lab_id) + '\\' + (str(program).replace(' ', '_')))
                except ValueError as ex:
                    su.move(path + '\\' + program, path + '\\Metadata')
                except FileExistsError:
                    pass
            elif str(program) == str(sys.argv[0]).split('\\')[-1] or str(program) == 'Result.csv':
                pass
            else:
                split_dict['Orphan'] = split_dict['Orphan'] + 1
        else:
            print('Broke')
            break

    print(split_dict)
except FileExistsError as fex:
    pass
           
for lab_section in sys.argv[2:-1]:
    folder_lab_section = path + '\\' + str(lab_section)
    print(folder_lab_section)
    try:
        open((lab_section + '.csv'), 'a').close()
    except PermissionError as pe:
        print(pe)
    with open((lab_section + '.csv'), 'w') as write_file:
        write_file.write('Name,Score/100,Score/75\n')
        for program_file in os.listdir(folder_lab_section):
            try:
                output = subproc.check_output('py ' + sys.argv[-1] + ' ' + folder_lab_section + '\\' + program_file, timeout=5)
                score = float((str(output).replace('\'', '').replace('\\r\\n', '\n').split('\n')[-2]).split(' ')[5])
                write_file.write(str(program_file).split('_')[-3] + ',' + str(score) + ',' + str(0.75 * score) + '\n')
            except Exception as ex:
                write_file.write(str(program_file).split('_')[-3] + ',' + 'N/A' + ',' + 'N/A' + '\n')
        write_file.close()