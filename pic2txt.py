from PIL import Image
import pytesseract

import inspect
import os
import sys

import requests

import pyperclip


def get_script_dir(follow_symlinks: bool = True) -> str:
    # https://clck.ru/P8NUA
    if getattr(sys, 'frozen', False):  # type: ignore
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)


def main():
    file_name = os.path.join(get_script_dir(), "temp_img")
    try:
        while True:
            # file = input("File: ")
            url_img = input("URL: ")
            lang = input("Lang: ")
            if not lang.isalpha():
                print("LangError")

                key = input("Continue?(y): ")
                if key == "y":
                    continue
                else:
                    os.remove(file_name)
                    break
            try:
                p = requests.get(url_img)
                out = open(file_name, "wb")
                out.write(p.content)
                out.close()

                text = pytesseract.image_to_string(
                    Image.open(file_name), lang=lang)
                print(text)

                pyperclip.copy(text)

            except FileNotFoundError:
                print("FileNotFoundError")
            except IsADirectoryError:
                print("FileNotFoundError")
            except pytesseract.pytesseract.TesseractError:
                print("PytesseractError")
            except requests.exceptions.MissingSchema:
                print("RequestsError:")

            key = input("Continue?(y): ")
            if key == "y":
                continue
            else:
                os.remove(file_name)
                break

    except KeyboardInterrupt:
        os.remove(file_name)
        print()
        return


if __name__ == "__main__":
    main()
