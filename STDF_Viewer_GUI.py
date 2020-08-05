import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from stdf.stdf_reader import Reader
from stdf.stdf_writer import Writer
import logging
from pathlib import Path
import time

class Table(QWidget):
    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
        # 设置标题与初始大小
        self.setWindowTitle('STDF Viewer Beta V0.1')
        self.resize(500, 300)

        row_num = len(stdf_dic)
        col_num = 4
        # 设置数据层次结构，4行4列
        self.model = QStandardItemModel(row_num, col_num)
        # 设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(['Index', 'Records', 'Count','Position'])

        # #Todo 优化2 添加数据
        # self.model.appendRow([
        #   QStandardItem('row %s,column %s' % (11,11)),
        #   QStandardItem('row %s,column %s' % (11,11)),
        #   QStandardItem('row %s,column %s' % (11,11)),
        #   QStandardItem('row %s,column %s' % (11,11)),
        # ])
        i=0
        j = 0
        last_rec = ''
        for key, val in stdf_dic.items():
            index_rec_list = key.split(' - ')
            index = index_rec_list[0]
            rec = index_rec_list[1]

            if rec == last_rec:
                j += 1
            else:
                j = 0
                index_item = QStandardItem(index)
                rec_item = QStandardItem(rec)
                pos_item = QStandardItem(val)
                cnt_item = QStandardItem(j)
                self.model.setItem(int(index), 0, index_item)
                self.model.setItem(int(index), 1, rec_item)
                self.model.setItem(int(index), 2, cnt_item)
                self.model.setItem(int(index), 3, pos_item)
            last_rec = rec
            # i +=1
            # if i==1000:
            #     break
        # for row in range(row_num):
        #     for column in range(col_num):
        #         temp_str =
        #         item = QStandardItem(temp_str) #QStandardItem('row %s,column %s' % (row, column))
        #         # 设置每个位置的文本值
        #         self.model.setItem(row, column, item)

        # 实例化表格视图，设置模型为自定义的模型
        self.tableView = QTableView()
        self.tableView.setModel(self.model)

        # #todo 优化1 表格填满窗口
        # #水平方向标签拓展剩下的窗口部分，填满表格
        # self.tableView.horizontalHeader().setStretchLastSection(True)
        # #水平方向，表格大小拓展到适当的尺寸
        # self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #
        # #TODO 优化3 删除当前选中的数据
        # indexs=self.tableView.selectionModel().selection().indexes()
        # print(indexs)
        # if len(indexs)>0:
        #   index=indexs[0]
        #   self.model.removeRows(index.row(),1)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.tableView)
        self.setLayout(layout)


def get_all_records(stdf):
    stdf.read_rec_list = True
    stdf_dic = {}
    i = 0
    for rec_name, position in stdf:
        stdf_dic[str(i) + ' - ' + rec_name] = position
        i += 1
    stdf.read_rec_list = False
    return stdf_dic

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    in_file = r'./sample_stdf/a595.stdf'
    stdf = Reader()
    stdf.load_stdf_file(stdf_file=in_file)
    stdf_dic = get_all_records(stdf)


    app = QApplication(sys.argv)
    table = Table()
    table.show()
    sys.exit(app.exec_())