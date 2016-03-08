import main as pyle
from pyle_sort import get_mod_datetime
import unittest
import os
import shutil
import random
import time
import string

TEST_DIR = "test_files/"
NUM_TEST_FILES = 42

def rand_string(size=6, chars=string.ascii_uppercase + string.digits):
    """
    http://stackoverflow.com/questions/2257441/
        random-string-generation-with-upper-case-letters-and-digits-in-python
    """
    return ''.join(random.choice(chars) for _ in range(size))

def rand_datetime_helper(start, end, format, prop):
    """
    http://stackoverflow.com/questions/553303/
        generate-a-random-date-between-two-other-dates

    Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)
    return time.mktime(time.localtime(ptime))

def rand_datetime(start, end, prop):
    """
    rand_datetime("1/1/2015 9:30 AM", "1/3/2015 2:30 PM", random.random())
    """
    return rand_datetime_helper(start, end, '%m/%d/%Y %I:%M %p', prop)

class Test_Pyle_Sort_Time(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(TEST_DIR):
            os.makedirs(TEST_DIR)
        for _ in range(NUM_TEST_FILES):
            file_name = rand_string()
            file_path = TEST_DIR + file_name
            curr = open(file_path, 'w')
            curr.write(file_path)
            curr.close()
            new_m_time = rand_datetime("1/1/2015 9:30 AM",
                                       "1/3/2020 2:30 PM",
                                       random.random())
            os.utime(file_path, (os.path.getctime(file_path),new_m_time))

    def tearDown(self):
        shutil.rmtree(TEST_DIR)

    def time_sort_launcher(self, step):
        params = "{'step':%s}" % repr(step)
        args = pyle.parser.parse_args(['sort', 'time', 'test_files',
                                       '--o', params])
        pyle.launcher(args)
        for directory in os.listdir(TEST_DIR):
            for filename in os.listdir(os.path.join(TEST_DIR, directory)):
                path = os.path.join(TEST_DIR, directory, filename)
                file_m_date = str(getattr(get_mod_datetime(path), step))
                error_msg = "Directory: %s, File date: %s do not match" \
                            % (directory, file_m_date)
                self.assertEqual(directory, file_m_date, error_msg)
        return

    def test_time_sort_day(self):
        return self.time_sort_launcher("day")
    #
    def test_time_sort_month(self):
        return self.time_sort_launcher("month")

    def test_time_sort_year(self):
        return self.time_sort_launcher("year")

    def test_time_sort_hour(self):
        return self.time_sort_launcher("hour")

    def test_time_sort_minute(self):
        return self.time_sort_launcher("minute")

    def test_time_sort_second(self):
        return self.time_sort_launcher("second")

class Test_Pyle_Sort_Ext(unittest.TestCase):
    def setUp(self):
        extensions = ["", ".", ".exe", ".io", ".zip", ".doc", ".pdf", ".123"]
        if not os.path.exists(TEST_DIR):
            os.makedirs(TEST_DIR)
        for _ in range(NUM_TEST_FILES):
            file_name = rand_string() + random.choice(extensions)
            file_path = TEST_DIR + file_name
            curr = open(file_path, 'w')
            curr.write(file_path)
            curr.close()

    def tearDown(self):
        shutil.rmtree(TEST_DIR)

    def ext_sort_launcher(self):
        args = pyle.parser.parse_args(['sort', 'ext', 'test_files'])
        pyle.launcher(args)
        for directory in os.listdir(TEST_DIR):
            for filename in os.listdir(os.path.join(TEST_DIR, directory)):
                path = os.path.join(TEST_DIR, directory, filename)
                ext = os.path.splitext(path)[1]
                error_msg = "Directory: %s, Extension: %s do not match" \
                            % (directory, ext)
                if directory == "Other":
                    error_msg = "%s Improperly sorted into Other" % (path)
                    self.assertTrue(len(ext) < 2, error_msg)
                else:
                    self.assertEqual(directory, ext, error_msg)
        return

    def test_ext_sort(self):
        return self.ext_sort_launcher()

if __name__ == '__main__':
    unittest.main()
