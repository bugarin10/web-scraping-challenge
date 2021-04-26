import numpy
from sklearn.linear_model import LinearRegression


def clean_list(list_):
    '''
    This function clean the list from html format
    '''
    result=[]
    for item in list_:  
        v1=item.find('>')
        v2=item.find('<',2)
        result.append(item[v1+1:v2])
    return result

def clean_list_url(list_):
    '''
    This function clean the list to to get the https
    '''
    result=[]
    for item in list_:  
        v1=item.find('href=')
        v2=item.find('>')
        item=item[v1+5:v2]
        item=item.replace("\"","")
        result.append(item)
    return result


def generate_b1_b0(dataframe,column_x,column_y):
    '''
    This function generates the constant and coefficient from a linear regression of two columns x and y.
    '''
    try:
        y=dataframe[column_y][~dataframe[column_y].isna()]
        x=dataframe[column_x][~dataframe[column_y].isna()]
        x=numpy.array(x).reshape((-1, 1))
        y=numpy.array(y)
        model = LinearRegression()
    
        model.fit(x, y)
        model = LinearRegression().fit(x, y)
        return [model.coef_[0],model.intercept_]
    except:
        print(f'There were problems with {column_x} and {column_y}')
        return[numpy.nan,numpy.nan]

def fill_nas(vector_y,vector_x,b1_b0):
    '''
    This function replace NAs with a predicted value greater or equal than zero
    '''
    try:
        result=vector_y.copy()
        cl=vector_y.isna()
        result[cl]=b1_b0[0]*vector_x+b1_b0[1]
        result[result<0]=0
        
        return result
    except:
        print(f'It didnt work for {vector_y} and {vector_x}, b1= {b1_b0[0]}')