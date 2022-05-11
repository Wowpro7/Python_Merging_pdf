import PyPDF2 as pypdf2
import os

# import pikepdf # alternative to pypdf2

MERGING_STYLES_LIST = ['Sequence', 'Middle Merger', 'Odd - Even', 'Cut', 'Spin Right', 'Spin Left']

class Rotation_error(Exception):
    pass

def check_files_type_validity(first_pdf_path=None, second_pdf_path=None):
    Files_are_valid = 'True'  # this way, because walking around with booleans was too much time consuming, and its
    # 03:16am, so deal with it_:)
    if first_pdf_path is not None:
        first_pdf_path = first_pdf_path.lower()
        if not first_pdf_path.endswith('.pdf'):
            Files_are_valid = first_pdf_path

    if second_pdf_path is not None:
        second_pdf_path = second_pdf_path.lower()
        if not second_pdf_path.endswith('.pdf'):
            if Files_are_valid == 'True':
                Files_are_valid = second_pdf_path
            else:
                Files_are_valid += ', ' + second_pdf_path

    return Files_are_valid


def check_files_accessibility(first_pdf_path, second_pdf_path):  #
    temp_dict = {"first_pdf_path": None, "first_pdf_pages_num": None, "second_pdf_path": None,
                 "second_pdf_pages_num": None}
    Error_message = None
    try:
        try:
            if first_pdf_path is not None:
                temp_dict["first_pdf_path"] = pypdf2.PdfFileReader(first_pdf_path)
                temp_dict["first_pdf_pages_num"] = temp_dict["first_pdf_path"].getNumPages()
        except pypdf2.utils.PdfReadError:
            Error_message = first_pdf_path
        finally:  # even if the first exception occurs always check the second file
            try:
                if second_pdf_path is not None:
                    temp_dict["second_pdf_path"] = pypdf2.PdfFileReader(second_pdf_path)
                    temp_dict["second_pdf_pages_num"] = temp_dict["second_pdf_path"].getNumPages()
            except pypdf2.utils.PdfReadError:  # both paths are not accessible, create an Error message
                if temp_dict["first_pdf_path"] is None:
                    Error_message += second_pdf_path + ', '
                else:
                    Error_message = second_pdf_path
                Error_message = Error_message + ',\n this file/s might be broken or password protected'

        return temp_dict, Error_message
    except FileNotFoundError as exp:
        return temp_dict, str(exp)
    except OSError:
	    return temp_dict, 'Your file source path is invalid, please check it'


def create_new_file_name(User_named, first_pdf_leads, first_pdf_path, second_pdf_path):
    if User_named is None:  # if the user asked for a specific name use it
        if first_pdf_leads:  # the first name determines the first page
            return "_{0}_and_{1}.pdf".format(first_pdf_path.split('.')[0], second_pdf_path.split('.')[0])
        else:
            return "_{1}_and_{0}.pdf".format(first_pdf_path.split('.')[0], second_pdf_path.split('.')[0])
    else:
        return "%s.pdf" % User_named


def odd_even_merge(pdf_1, pdf_1_page_num, pdf_2, pdf_2_page_num, new_pdf, first_pdf_leads=True):
    count_1 = 0
    count_2 = 0

    if pdf_1_page_num > pdf_2_page_num:  # compare files pages size to know how many times to run the loop
        run_pages = pdf_1_page_num
    else:
        run_pages = pdf_2_page_num

    for i in range(run_pages):  # run through all the pages

        if first_pdf_leads:  # if its True
            if pdf_1_page_num > count_1:
                new_pdf.addPage((pdf_1.getPage(count_1)))
                count_1 += 1
            if pdf_2_page_num > count_2:
                new_pdf.addPage((pdf_2.getPage(count_2)))
                count_2 += 1

        else:
            if pdf_2_page_num > count_2:
                new_pdf.addPage((pdf_2.getPage(count_2)))
                count_2 += 1
            if pdf_1_page_num > count_1:
                new_pdf.addPage((pdf_1.getPage(count_1)))
                count_1 += 1
    return new_pdf


def merge_in_sequence(pdf_1, pdf_1_page_num, pdf_2, pdf_2_page_num, new_pdf, first_pdf_leads=True):
    count_1 = 0
    count_2 = 0

    sum_pages_value = pdf_1_page_num + pdf_2_page_num

    for i in range(sum_pages_value):  # run through all the pages

        if first_pdf_leads:  # if its True start with the first pdf
            if pdf_1_page_num > count_1:
                new_pdf.addPage((pdf_1.getPage(count_1)))
                count_1 += 1

            if pdf_1_page_num == count_1:  # when finished running over all the pdf switch the "first_pdf_leadss" boolean value to continue with the other file
                first_pdf_leads = not first_pdf_leads

        else:
            if pdf_2_page_num > count_2:
                new_pdf.addPage((pdf_2.getPage(count_2)))
                count_2 += 1

            if pdf_2_page_num == count_2:  # when finished running over all the pdf switch the "first_pdf_leadss" boolean value to continue with the other file
                first_pdf_leads = not first_pdf_leads
    return new_pdf


def merge_in_the_middle(pdf_1, pdf_1_page_num, pdf_2, pdf_2_page_num, new_pdf, start_page,
                        first_pdf_leads=True):
    count_1 = 0
    count_2 = 0

    if first_pdf_leads:
        if start_page > pdf_1_page_num:
            return None
    else:
        if start_page > pdf_2_page_num:
            return None

    sum_pages_value = pdf_1_page_num + pdf_2_page_num
    file_current_mering_part = 1  # it can be up tp 3 parts (starting from 1)

    for i in range(sum_pages_value):  # run through all the pages
        if file_current_mering_part == 1:
            if first_pdf_leads:  # if its True start with the first pdf
                if start_page > count_1:
                    new_pdf.addPage((pdf_1.getPage(count_1)))
                    count_1 += 1

                if start_page == count_1:
                    file_current_mering_part = 2

            else:
                if start_page > count_2:
                    new_pdf.addPage((pdf_2.getPage(count_2)))
                    count_2 += 1

                if start_page == count_2:
                    file_current_mering_part = 2

        elif file_current_mering_part == 2:
            if not first_pdf_leads:  # if its True start with the first pdf
                if pdf_1_page_num > count_1:
                    new_pdf.addPage((pdf_1.getPage(count_1)))
                    count_1 += 1

                if pdf_1_page_num == count_1:
                    file_current_mering_part = 3

            else:
                if pdf_2_page_num > count_2:
                    new_pdf.addPage((pdf_2.getPage(count_2)))
                    count_2 += 1

                if pdf_2_page_num == count_2:
                    file_current_mering_part = 3

        elif file_current_mering_part == 3:
            if first_pdf_leads:  # if its True start with the first pdf
                if pdf_1_page_num > count_1:
                    new_pdf.addPage((pdf_1.getPage(count_1)))
                    count_1 += 1

            else:
                if pdf_2_page_num > count_2:
                    new_pdf.addPage((pdf_2.getPage(count_2)))
                    count_2 += 1

    return new_pdf


def merge_cut_pages_off(pdf_1, pdf_1_page_num, start_page, stop_page, new_pdf):
    for i in range(start_page, stop_page + 1):
        new_pdf.addPage((pdf_1.getPage(i)))

    return new_pdf


def Spin(pdf_1, pdf_1_page_num, Spin_Right, new_pdf, pages_and_rotating_degree):
    """
    :param pages_and_rotating_degree: expected syntax:
        options:
        1. one page: "1:90" , "<page_number>:<rotate_degree>"
        2. two page or more: "1-n:90" , "<start_page-stop_page>:<rotate_degree>"
        3. different pages different rotating degrees: "1-90,4-9:270" , "<page_number>:<rotate_degree>,<start_page-stop_page>:<rotate_degree>"
    """

    # TODO:
    '''
    1. split the groups of rotation: <>.split(',') = creating all the groups of pages needed to rotate
    2. run For loop over all the list
    3. every index in this list split it to page/s and rotating degree: <>.split(':') = creating a list that contains a page/s to rotate and the degree
    4. check if the page/s has '-' symbol, if it does split it: <>.split('-') creating 2 items of range to run over.
    else if doesnt have it rotate the page
    '''
    Rotate_degree_options_list=[0, 90, 180, 270, 360] # the only possible rotating degree
    dictionary_of_rotating_pages = {}
    try:
        list_of_rotating_groups = pages_and_rotating_degree.split(',')  # creating a list of all the rotating groups
        for group in list_of_rotating_groups:
            pages_range, rotating_degree = group.split(':')  # split the group to see the pages range and rotating degree
            rotating_degree = int(rotating_degree)
            if rotating_degree not in  Rotate_degree_options_list:
                raise Rotation_error("You can rotate only in: 0,90,180,270,360 degrees.")
            if '-' in pages_range:
                start_page, stop_page = pages_range.split('-')  # fetching start and stop page
                start_page = int(start_page) - 1
                stop_page = int(stop_page) - 1
                if start_page < 0 or start_page >= pdf_1_page_num or stop_page < 0 or stop_page >= pdf_1_page_num:
                    return 'Your requested page is illegal.\nThere is not enough pages in the file or its below 1.'
                dictionary_of_rotating_pages |= dict.fromkeys(list(range(start_page, stop_page + 1)), rotating_degree)
                # for i in range(int(start_page), int(stop_page)+1):
                # new_pdf.addPage(pdf_1.getPage(i).rotateClockwise(int(rotating_degree)))
            else:
                # new_pdf.addPage(pdf_1.getPage(int(pages_range)).rotateClockwise(int(rotating_degree)))
                pages_range = int(pages_range) - 1
                if pages_range < 0 or pages_range >= pdf_1_page_num :
                    return 'Your requested page is illegal.\nThere is not enough pages in the file or its below 1.'
                dictionary_of_rotating_pages |= {pages_range : rotating_degree}

    except Rotation_error as exp:
        return str(exp)

    except Exception:
        return 'try this format for start page: \n<page_number>:<degree(90,180,270)>,<start_page-stop_page>:<degree(90,180,270)>' #'something went horrible wrong, check your page range syntax. refer to: File->Help'

    # TODO:
    '''
    need to run a over all the pdf and change only the requested pages.
    1.initate with creating a dictionary: { [pages_range_list]:degree,....}
    2. run a for loop over all the pages of the pdf.
    3. check if the page is in one of the keys, if yes tha use its valuse to knnow if to rotate else just add the page and continue
    '''
    for i in range(pdf_1_page_num):
        if i in dictionary_of_rotating_pages.keys():
            if Spin_Right:
                new_pdf.addPage(pdf_1.getPage(i).rotateClockwise(dictionary_of_rotating_pages[i]))
            else:
                new_pdf.addPage(pdf_1.getPage(i).rotateCounterClockwise(dictionary_of_rotating_pages[i]))
        else:
            new_pdf.addPage(pdf_1.getPage(i))
    return new_pdf


def define_merging_style(merging_style):
    odd_even = None
    Sequence = None
    Middle = None
    cut = None
    Spin_right = None
    Spin_left = None

    for i in merging_style.keys():
        if i == 'Sequence':
            Sequence = merging_style[i]
        elif i == 'Middle Merger':
            Middle = merging_style[i]
        elif i == 'Odd - Even':
            odd_even = merging_style[i]
        elif i == 'Cut':
            cut = merging_style[i]
        elif i == 'Spin Right':
            Spin_right = merging_style[i]
        elif i == 'Spin Left':
            Spin_left = merging_style[i]

    return odd_even, Sequence, Middle, cut, Spin_left, Spin_right


# def merge(first_pdf_path, second_pdf_path, saving_path=None, first_pdf_leads=True, User_named=None, odd_even=None, Sequence=None,
#  Middle=None, start_page=None):  # merger two files.. Previous version before the use of tuple

def merge(first_pdf_path, second_pdf_path, saving_path=None, first_pdf_leads=True, User_named=None, merging_style={},
          start_page=None, stop_page=None):  # merger two files

    odd_even, Sequence, Middle, cut, Spin_left, Spin_right = define_merging_style(merging_style)

    filename = check_files_type_validity(first_pdf_path, second_pdf_path)
    if filename != 'True':
        return "*** '%s' file/s is invalid ***" % filename

    # basic information all functions need: - received at the function call
    # checking for file validation for use
    file_access, Error_message = check_files_accessibility(first_pdf_path, second_pdf_path)
    if Error_message is not None:
        return Error_message
    else:
        pdf_1 = file_access["first_pdf_path"]
        pdf_1_page_num = file_access["first_pdf_pages_num"]
        pdf_2 = file_access["second_pdf_path"]
        pdf_2_page_num = file_access["second_pdf_pages_num"]

    new_pdf = pypdf2.PdfFileWriter()

    # basic information returned by all function:s
    if odd_even:  # merge page by page from different files
        new_pdf = odd_even_merge(pdf_1, pdf_1_page_num, pdf_2, pdf_2_page_num, new_pdf, first_pdf_leads)
    elif Sequence:  # sequential merge
        new_pdf = merge_in_sequence(pdf_1, pdf_1_page_num, pdf_2, pdf_2_page_num, new_pdf, first_pdf_leads)
    elif cut:  # cut pages from the original pdf file and create an new file
        if start_page > pdf_1_page_num or start_page > stop_page:
            return 'Error: Starting page is bigger than the number of pages available'

        if start_page > stop_page:
            return 'Error: Starting page is bigger than the Stop page'

        if stop_page > pdf_1_page_num:
            return 'Error: Stop page is bigger than the number of pages available'

        new_pdf = merge_cut_pages_off(pdf_1, pdf_1_page_num, start_page, stop_page, new_pdf)
    elif Spin_right or Spin_left:
        pages_and_rotating_degree = start_page
        new_pdf = Spin(pdf_1, pdf_1_page_num, Spin_right, new_pdf, pages_and_rotating_degree)
    elif Middle:  # merge in at starting page
        if first_pdf_path:
            if pdf_1_page_num < start_page:
                return "Middle page pause value is too high"
            elif start_page == 0:
                return "start page cant be 1"
        else:
            if pdf_2_page_num < start_page:
                return "Middle page pause value is too high"

        new_pdf = merge_in_the_middle(pdf_1, pdf_1_page_num, pdf_2, pdf_2_page_num, new_pdf, start_page,
                                      first_pdf_leads)
    else:
        return "***ERROR 404 - You Fucked up, choose an option for merging***"

    new_pdf_name = create_new_file_name(User_named, first_pdf_leads, first_pdf_path, second_pdf_path)
    # new_pdf.encrypt(user_pwd="123", owner_pwd="123", use_128bit=True)
    #pdf_1.close()  # close all the opened files
    #pdf_2.close()

    try:
        with open(saving_path+new_pdf_name, 'wb') as pdf:  # create the file
            new_pdf.write(pdf)
    except PermissionError as exp:
        return str(exp) + '\n choose a different saving path'
    except FileNotFoundError:
        return 'Your saving path is invalid, please try a different path'
    except TypeError and AttributeError:
        return new_pdf
    else:
        return new_pdf_name


# TODO:
"""
make the code better looking
"""


# def main():
#     #
#     #
#     merging_style = {'Spin Right': True}
#     file_name = merge(User_named="yea_boio", merging_style=merging_style, first_pdf_path="SignalTap 2.pdf",
#                       second_pdf_path='SignalTap 2.pdf', start_page='1-3:90,4:180')
#
#     #
#     print("file name: '%s' , is ready for usage" % file_name)


#
#
# if __name__ == '__main__':
#     main()
