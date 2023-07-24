from sklearn.ensemble import RandomForestClassifier

def build_model(n_estimators=500,
          criterion='log_loss',
          max_dept=4,
          min_samples_split=2,
          min_samples_leaf=2):
    model = RandomForestClassifier(n_estimators=n_estimators,
                                   criterion=criterion,
                                   max_depth=max_dept,
                                   min_samples_split=min_samples_split,
                                   min_samples_leaf=min_samples_leaf
                                   )
    return model


def training(model, Xtrain, ytrain):
    history = model.fit(Xtrain, ytrain)
    print('Saving the model ...')
    model.save('RandomForestClassifer.h5')
    return model, history