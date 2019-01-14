import os
from datetime import datetime

from ..test_client import TestBase
from ...services.chart_service import draw_chart, build_file_name, get_chart_data


class TestChartService(TestBase):

    def test_draw_chart(self):
        """
        Tests that a chart can be generated and saved
        """
        name = 'tests/products/testName.png'
        draw_chart(self.first_date.isoformat(), self.second_date.isoformat(), name)
        assert os.path.isfile(name)

    def test_build_file_name(self):
        """
        Tests that a file name can be successfully built
        """
        now = datetime.now().strftime('%Y-%m-%d-%H')
        correct_file_name = "static/plots/testEtag2018-11-192018-11-21" + now + ".png"
        test_file_name = build_file_name(self.first_date, self.second_date)
        assert correct_file_name == test_file_name

    def test_get_chart_data(self):
        """
        Tests that we can retrieve the necessary data for a chart
        """
        mins, names, colours = get_chart_data(self.second_date, self.first_date)
        assert mins == [2880, 2880]
        assert names == ['test@test.com', 'test1@test.com']
        assert colours == ['1', '2']
