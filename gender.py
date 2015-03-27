__author__ = 'maru'


class UserGender(object):

    def __init__(self, gen_files):
        super(UserGender, self).__init__()
        self.male = None
        self.female = None
        self.unknown = None
        self.file_dir = gen_files
        self.top = 1000
        self.load_files()

    def get_names(self, file_name):
        import os.path

        if not os.path.isfile(file_name):
            raise Exception("Oops, %s is not a file" % file_name)

        f = open(file_name)
        with f:
            lines = f.readlines()

        fem = [l.strip().split("\t") for l in lines] #discard first lines
        names = [name[0] for name in fem[:self.top]]
        return names

    def load_files(self):
        dir_fem = self.file_dir + "/dist.female.first.txt"
        self.female = self.get_names(dir_fem)
        dir_mas = self.file_dir + "/dist.male.first.txt"
        self.male = self.get_names(dir_mas)

    def get_female_index(self, name):
        fem = None
        try:
            fem = self.female.index(name)
        except ValueError:
            return None
        except:
            raise ValueError("We cannot identify this name")
        return fem

    def get_male_index(self, name):
        mas = None
        try:
            mas = self.female.index(name)
        except ValueError:
            # import sys
            # return sys.maxint
            return None
        except:
            raise ValueError("We cannot identify this name")
        return mas

    def get_gender(self, name):
        fem = self.get_female_index(name)
        mas = self.get_male_index(name)
        try:
            if fem is None and mas is None:
                return None
            if fem < mas:
                return "female"
            else:
                return "male"
        except ValueError:
            return None
        except:
            raise ValueError("We cannot identify this name")