from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import roc_curve, roc_auc_score 

def train_classifier(classifier, X, y, groups):
    '''
    Uses leave one session out cross validation
    '''

    logo = LeaveOneGroupOut()

    predictions = []
    true = []
    fprs = []
    tprs = []
    aucs = []
    betas = []

    for train_index, test_index in logo.split(X, y, groups):
        classifier.fit(X[train_index], y[train_index])
        prediction, fpr, tpr, auc, beta = assess_classifier(classifier, X[test_index], y[test_index])

        predictions.append(prediction)
        true.append(y[test_index])
        fprs.append(fpr)
        tprs.append(tpr)
        aucs.append(auc)
        betas.append(beta)

    return predictions, true, fprs, tprs, aucs, betas


def assess_classifier(classifier, test_data, test_targets):
    prediction = classifier.predict_proba(test_data)

    fpr, tpr, thresh = roc_curve(test_targets, prediction[:, 1])

    auc = roc_auc_score(test_targets, prediction[:, 1])

    beta = classifier.coef_

    return prediction, fpr, tpr, auc, beta
