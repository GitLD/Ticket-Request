# Ticket-Request
## Description
A ticket request for 12306 client on cmd
## Usage
Under the directory:  
python tickets.py -h : to see the help doc  

Usage:  
	tickets [-gdtkz] <from> <to> <date>  
	
Options:  
	-h,--help		显示帮助菜单  
	-g			高铁  
	-d			动车  
	-t			特快  
	-k			快速  
	-z			直达  
	
Example:  
	tickets 北京 上海 2016-10-10  
  	tickets -dg 成都 南京 2016-10-10  
## Some attention:  
-The date input must have the train data, otherwise an error will occur.  
-There has been no processing for the bad net connect, so when you can't link it will also raise an error.  


