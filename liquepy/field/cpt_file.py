import numpy as np
# from liquepy.exceptions import deprecation
import ntpath


# def load_cpt_data(fname):
#     deprecation('Deprecated (load_cpt_data), should use load_cpt_from_file')
#
#     # import data from csv file
#     data = np.loadtxt(fname, skiprows=24, delimiter=";")
#     depth = data[:, 0]
#     q_c = data[:, 1] * 1e3  # should be in kPa
#     f_s = data[:, 2]
#     u_2 = data[:, 3]
#     gwl = None
#     infile = open(fname)
#     lines = infile.readlines()
#     for line in lines:
#         if "Assumed GWL:" in line:
#             gwl = float(line.split(";")[1])
#
#     return depth, q_c, f_s, u_2, gwl


def load_cpt_from_file(ffp, delimiter=";"):
    # import data from csv file
    folder_path, file_name = ntpath.split(ffp)
    data = np.loadtxt(ffp, skiprows=24, delimiter=delimiter, usecols=(0, 1, 2, 3))
    depth = data[:, 0]
    q_c = data[:, 1] * 1e3  # should be in kPa
    f_s = data[:, 2]
    u_2 = data[:, 3]
    gwl = None
    a_ratio = None
    infile = open(ffp)
    lines = infile.readlines()
    for line in lines:
        if "Assumed GWL:" in line:
            gwl = float(line.split(delimiter)[1])
        if "aratio" in line:
            try:
                a_ratio = float(line.split(delimiter)[1])
            except ValueError:
                pass
    return CPT(depth, q_c, f_s, u_2, gwl, a_ratio, folder_path=folder_path, file_name=file_name, delimiter=delimiter)


class CPT(object):
    def __init__(self, depth, q_c, f_s, u_2, gwl, a_ratio=None, folder_path="<path-not-set>", file_name="<name-not-set>",
                 delimiter=";"):
        """
        A cone penetration resistance test

        Parameters
        ----------
        depth: array_like
            depths from surface
        q_c: array_like, [kPa]
        f_s: array_like, [kPa]
        u_2: array_like, [kPa]
        gwl: float, [m]
            ground water level
        a_ratio: float,
            Area ratio
        """
        self.depth = depth
        self.q_c = q_c
        self.f_s = f_s
        self.u_2 = u_2
        self.gwl = gwl
        self.a_ratio = a_ratio
        self.folder_path = folder_path
        self.file_name = file_name
        self.delimiter = delimiter


    @property
    def q_t(self):
        """
        Pore pressure corrected cone tip resistance

        """
        # qt the cone tip resistance corrected for unequal end area effects, eq 2.3
        return self.q_c + ((1 - self.a_ratio) * self.u_2)
