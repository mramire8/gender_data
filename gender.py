__author__ = 'maru'
import sys


class UserGender(object):

    def __init__(self, gen_files):
        super(UserGender, self).__init__()
        self.male = None
        self.female = None
        self.unknown = None
        self.file_dir = gen_files
        self.top = 1000
        self.load_files()

    def get_file_lines(self, file_name):
        import os.path

        if not os.path.isfile(file_name):
            raise Exception("Oops, %s is not a file" % file_name)

        f = open(file_name)
        with f:
            lines = f.readlines()
        return lines

    def get_names(self, lines):

        fem = [l.strip().split() for l in lines] #discard first lines
        names = [name[0] for name in fem[:self.top]]
        return names

    def load_files(self):
        if self.file_dir is not None:
            dir_fem = self.file_dir + "/dist.female.first.txt"
            dir_mas = self.file_dir + "/dist.male.first.txt"
            females = self.get_file_lines(dir_fem)
            males = self.get_file_lines(dir_mas)
        else:
            import requests
            males = requests.get('http://www2.census.gov/topics/genealogy/1990surnames/dist.male.first').text.split('\n')
            females = requests.get('http://www2.census.gov/topics/genealogy/1990surnames/dist.female.first').text.split('\n')

        self.female = self.get_names(females)
        self.male = self.get_names(males)

    def get_female_index(self, name):
        fem = None
        try:
            fem = self.female.index(name)
        except ValueError:
            return sys.maxint
            # return None
        except:
            raise ValueError("We cannot identify this name")
        return fem

    def get_male_index(self, name):
        mas = None
        try:
            mas = self.male.index(name)
        except ValueError:
            return sys.maxint
            # return None
        except:
            raise ValueError("We cannot identify this name")
        return mas

    def get_gender(self, name):
        fem = self.get_female_index(name.upper())
        mas = self.get_male_index(name.upper())
        try:
            if fem is sys.maxint and mas is sys.maxint:
                return None
            if fem < mas:
                return "female"
            elif mas < fem:
                return "male"
        except ValueError:
            return None
        except:
            raise ValueError("We cannot identify this name")