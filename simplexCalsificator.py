import pandas as pd
import numpy as np
import copy

class simplexClassificator:
  def __init__(self, measure):
    self.measure = measure
    self.complexes = {}
  def fit(self, X, y):
    X = self.one_hot_encode(X)
    
    y_unique = list(y.unique())
    for i in range(len(y_unique)):
      self.complexes[y_unique[i]] = []

    for index in range(len(y)):
      self.complexes[y.iloc[index]] += [index]

    for i in range(len(y_unique)):
      self.complexes[y_unique[i]] = X.iloc[self.complexes[y_unique[i]]].reset_index(drop=True)

  def predict(self, x):
    x = self.one_hot_encode(x)
    self.pred = copy.deepcopy(self.complexes)

    for column in self.pred:
      self.pred[column] = pd.concat([self.pred[column], x], sort=False).reset_index(drop=True).fillna(0).astype('uint8')

    prediction = 'NaP'
    integration = 0
    temp = 0
    
    for clasification in self.pred:
      
      matrix = np.array(self.pred[clasification])
    #  print('matriz', matrix)
      transposed_matrix = matrix.transpose()
    #  print('trans', transposed_matrix)
      MVC = np.matmul(matrix,transposed_matrix)
    #  print('mvc', MVC)
      MCC = np.array(self.calculateMCC(MVC))
    #  print('mcc', MCC)

      if self.measure == 'concentricity':
        
        temp = self.concentricity(MVC, len(MVC)-1)
      elif self.measure == 'degree':
        temp = self.loopfor(MCC, len(MCC)-1)

      elif self.measure == 'maximal':
       temp = self.adyacenciaMaximalSimplicial(MCC, len(MCC)-1)
        # print('maximal', temp)
      
      if temp > integration:
        integration = temp
        prediction = clasification

    return prediction

  def one_hot_encode(self, input):
    for column in input:

      if input[column].dtype.name == 'category':
        input = pd.concat([input, pd.get_dummies(input[column], prefix=column)], axis=1, join='inner')
        input.drop(column, inplace=True, axis=1)
      else:
        input[column] = input[column].astype('uint8')
    return input

  #Se pide la matriz MVC y se pide el numero de fila del simplice 
  def concentricity(self, MVC, row):
    total = 0
    filas = len(MVC)
    columns = len(MVC[row])

    for c in range(columns) :
      if(c != row ):
        total += MVC[row][c]
        
    return total

  #MCC se le resta una matriz de 1 a MVC
  def calculateMCC (self, MVC):
    #for r in range(len(MVC)) :
    #  for c in range(len(MVC[r])) :
    #    MVC[r][c] = MVC[r][c] - 1
    return MVC - 1

  #Centralidad de grado la matriz en MCC y la fila del simplice
  def loopfor(self, MCC, row):
    total = 0
    v = MCC[row][row]
    for q in range(v+1) :
      for i in range(len(MCC[row])) :
        if(MCC[row][i] >= q and i != row):
          total = total + 1
    
    return total

  #Adyacencia Maximal con MCC, n siendo dimension de MCC y row la fila del simplice
  def adyacenciaMaximal(self, MCC, row):
    sigma = MCC[row][row]
    sigma = sigma -1 
    column_matrix = np.transpose(MCC)
    gramax = 0
    p_adyacente_final =[]

    for p in range(sigma +1):
      p_adyacent_columns = []
      for c in range(len(MCC[row])) :
        if(c != row and MCC[row][c] == p  ):
          p_adyacent_columns.append(c)

      #print('p adjacent columns', p_adyacent_columns)
      for selected_column in (p_adyacent_columns):
        for matrix_columns in range(len(column_matrix)):
          if(selected_column != matrix_columns and column_matrix[matrix_columns][matrix_columns] == (row + column_matrix[selected_column][selected_column]) - p and  column_matrix[selected_column][selected_column] == column_matrix[selected_column][matrix_columns]) :
            p_adyacente_final.append(selected_column)
            break
            
          if(column_matrix[selected_column][selected_column] == column_matrix[selected_column][matrix_columns] and selected_column != matrix_columns):
            p_adyacente_final.append(selected_column)
            break

      gramax += len(p_adyacent_columns) - len(p_adyacente_final)
      # print('gramax', gramax)

    return gramax
  
  #Adyacencia Maximal Superior toma 
  def adyacenciaMaximalSuperior(self, MCC , row):
    n = len(MCC)
    Dim = 0
    column_matrix = np.transpose(MCC)
    gramasu = 0
    p_adyacent_columns = []
    p_adyacent_columns_final = []

    for k in range(n):
      sigma = MCC[k][k]
      if(sigma > Dim ):
        Dim = sigma

    #print('resta', Dim - MCC[row][row])
    #print('dim', Dim)
    #print('mcc', MCC[row][row])
    for r in range(Dim - MCC[row][row]):
      #print('paso')

      p_adyacent_columns = []
      for c in range(len(column_matrix)):
        if(column_matrix[c][c] == row+r+2):
          p_adyacent_columns.append(c)
  
      #print('p adjacent columns superior', p_adyacent_columns)
      for columns in p_adyacent_columns:
      
        if MCC[row][columns] != MCC[row][row]:
        
          p_adyacent_columns_final.append(columns)
          break

    
      for columns in (p_adyacent_columns):
      
        columns_amount = 0
        for c in range(len(column_matrix)):
          if(MCC[columns][c] == row + r+1):
            columns_amount = columns_amount + 1
        if(columns_amount >= 2) :
          p_adyacent_columns_final.append(columns)
          break

      gramasu += len(p_adyacent_columns)-len(p_adyacent_columns_final)
      # print('gramasu', gramasu)
  
    return gramasu

  def adyacenciaMaximalSimplicial(self, MCC, row) :
    adyacencia_Maximal = self.adyacenciaMaximal(MCC,row)
    adyacencia_maximal_superior = self.adyacenciaMaximalSuperior(MCC,row)
    # print('total gramasu', adyacencia_maximal_superior)
    return adyacencia_Maximal+ adyacencia_maximal_superior

  def score(self, X, y):
    cc = 0
    for count in range(len(X)):
      t = X.iloc[[count]]
      r = self.predict(t)
      if r == y[count]:
        cc += 1

    return cc/range(len(X))