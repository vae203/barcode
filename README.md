# barcode

1.程序运行要求

    python==3.6.4
    
    依赖库：
    
        numpy
        
        math
        
        time
        
        argparse
        
2.程序运行方法

    usage: barcode.py [-h] group_num group_len barcode_len rate repeat_num min_dist
    
    positional arguments:
    
      group_num    组数: 例如为5
      
      group_len    每组的barcode个数: 例如为16
      
      barcode_len  barcode长度: 例如为10
      
      rate         组内每列每种碱基最小占比: 例如为0.125
      
      repeat_num   不允许相同碱基连续重复个数: 例如为3
      
      min_dist     最小humming距离: 例如为3
      
    optional arguments:
    
      -h, --help   show this help message and exit
      
    例如：python barcode.py 5 16 10 0.125 3 3
    
3.程序编写思路

   1）按组生成barcodes，先满足每列碱基最小占比
   
   2）对生成的当前组进行判断，是否满足humming距离和不允许相同碱基连续重复个数;若满足不满足则继续生成
   
   3）按组打印所有barcodes
 
   
 

      
