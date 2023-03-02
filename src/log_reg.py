from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
import pandas as pd

def myLogRegression(featureList, df, testShare = 0.25, resampling = False, ):
  df['revert'] = pd.to_numeric(df['revert'], downcast='integer')
  if len(featureList) == 1:
      X_train, X_test, y_train, y_test = train_test_split(df[featureList[0]].array.reshape(-1, 1), df['revert'].values.ravel(), test_size=testShare, random_state=0)    
  else:
      X_train, X_test, y_train, y_test = train_test_split(df[featureList], df['revert'].values.ravel(), test_size=testShare, random_state=0)
  
  if resampling: #then we will actually change the train data only, but not the test data!
    if(len(featureList)) == 1:       
      X_train = pd.DataFrame(X_train[0], index=range(0,len(y_train))) #we need this to be a dataframe. Yes this looks weird but the test_train_split operates with nonintuitive arrays
    y_train = pd.DataFrame(y_train,index=X_train.index, columns=['revert'])
    df_train = pd.concat([X_train, y_train],axis=1 )
    meanRR = df_train['revert'].mean()
    df_train['Weight'] = df_train['revert'].apply(lambda x: 1/meanRR if x == 1 else 1)    
    df_train['Weight'] = df_train['Weight'].astype(object)    
    df_train = df_train.sample(n=100000, replace=True, weights='Weight') #resampling with constant size 100k for now    
    X_train = df_train.loc[:, (df_train.columns != 'revert') & (df_train.columns != 'Weight')]
    y_train = df_train['revert']
    

  myLogiReg= LogisticRegression()
  myLogiReg.fit(X_train, y_train)
  print("Reg coefficients - sklearn")
  print(myLogiReg.intercept_)
  print(myLogiReg.coef_)
  
  ##also use statmodels for some extra interesting statistics
  import statsmodels.api as sm
  X_sm = sm.add_constant(X_train) #have to add intercept manually for statmodels    
  logit_model=sm.Logit(y_train, X_sm)
  
  result=logit_model.fit()
  print("Summary regression - statmodels")
  print(result.summary2())  

  y_pred = myLogiReg.predict(X_test)
  #print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(myLogiReg.score(X_test, y_test))) #this seems useless
  
  from sklearn.metrics import confusion_matrix
  confusion_matrix = confusion_matrix(y_test, y_pred)
  print("Confusion matrix")
  print(confusion_matrix)

  from sklearn.metrics import classification_report
  print("Classification report")
  print(classification_report(y_test, y_pred))
  
  from sklearn.metrics import roc_auc_score, roc_curve
  logit_roc_auc = roc_auc_score(y_test, myLogiReg.predict(X_test)) #later, implement cross validation here https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html
  fpr, tpr, thresholds = roc_curve(y_test, myLogiReg.predict_proba(X_test)[:,1])
  import matplotlib.pyplot as plt 
  plt.figure()
  plt.plot(fpr, tpr, label='Logistic Regression (area = %0.3f)' % logit_roc_auc)
  plt.plot([0, 1], [0, 1],'r--')
  plt.xlim([0.0, 1.0])
  plt.ylim([0.0, 1.05])
  plt.xlabel('False Positive Rate')
  plt.ylabel('True Positive Rate')
  plt.title('Receiver operating characteristic')
  plt.legend(loc="lower right")
  #plt.savefig('Log_ROC')
  plt.show()

  #myLogiRegFinal= LogisticRegression()
  #myLogiRegFinal.fit(df[featureList], df['revert'].values.ravel())
  return myLogiReg