from sklearn import metrics
from tqdm import trange, tqdm
import torch
from config import config

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

batch_size = config.batch_size

def get_accuracy(y_true, y_pred):
    return metrics.accuracy_score(y_true, y_pred)


def get_f1(y_true, y_pred, average='macro'):
    return metrics.f1_score(y_true, y_pred, average=average)


def train_model(train_dataloader, model, optimizer, scheduler, loss_fcn, num_epochs=5, 
    evaluate=False, val_dataloader=None, write_logs=False):
    if write_logs:
        f = open('train_logs.txt', 'w')
        f.write('Train Accuracy\tTraining Loss\tTraining F1\tVal Accuracy\tVal Loss\tVal F1\n')
        step_losses = []
        step_acc = []
    
    for epoch in trange(num_epochs, desc='Epoch'): 
        model.train()
        total_loss = 0.0
        y_predicted = []
        y_true = []
        for step, (images, labels) in enumerate(tqdm(train_dataloader, desc="Iteration")):
            labels = labels.to(device)
            images = images.to(device)
            #images = images.view(-1, input_size)
            optimizer.zero_grad()
            outputs = model(images)
            _, y_pred = torch.max(outputs, 1)
            y_predicted.extend(y_pred.cpu().tolist())
            y_true.extend(labels.cpu().tolist())
            loss = loss_fcn(outputs, labels)

            loss.backward()
            optimizer.step()
            step_loss = loss.item() / batch_size
            total_loss += step_loss
            step_train_acc = get_accuracy(y_true, y_predicted)
            step_losses.append(step_loss)
            step_acc.append(step_train_acc)

        train_acc = get_accuracy(y_true, y_predicted)
        train_loss = total_loss / len(train_dataloader)
        train_f1 = get_f1(y_true, y_predicted)

        print('Training accuracy: %f' % (train_acc))
        print('Training loss: %f' % (train_loss))
        print('Training f1 score: %f' % (train_f1))

        if evaluate:
            eval_acc, eval_loss, eval_f1 = eval_model(val_dataloader, model, loss_fcn)

        if write_logs:
            # f.write('Training accuracy: %f\tTraining loss: %f\tTraining f1 score: %f\n' % (train_acc, train_loss, train_f1))
            # f.write('Validation accuracy: %f\tValidation loss: %f\tValidation f1 score: %f\n' % (eval_acc, eval_loss, eval_f1))
            f.write('%f\t%f\t%f\t%f\t%f\t%f\n' % (train_acc, train_loss, train_f1, eval_acc, eval_loss, eval_f1))


        if scheduler:
            scheduler.step()

    save_path = './saved_model_' + str(epoch)
    torch.save(model.state_dict(), save_path)

    if write_logs:
        f.close()
        assert len(step_losses) == len(step_acc)
        with open('step_train_logs.txt', 'w') as f2:
            f2.write('Train Accuracy\tTrain Loss\n')
            for i in range(len(step_losses)):
                f2.write('%f\t%f\n' % (step_acc[i], step_losses[i]))




def eval_model(val_dataloader, model, loss_fcn, plot=False):
    model.eval()
    with torch.no_grad():
        total_loss = 0.0
        y_predicted = []
        y_true = []
        for step, (images, labels) in enumerate(tqdm(val_dataloader, desc="Iteration")):
            images = images.to(device)
            labels = labels.to(device)
            # images = images.view(-1, input_size)
            outputs = model(images)
            _, y_pred = torch.max(outputs, 1)
            y_predicted.extend(y_pred.cpu().tolist())
            y_true.extend(labels.cpu().tolist())
            loss = loss_fcn(outputs, labels)
            total_loss += (loss.item() / batch_size)

        acc = get_accuracy(y_true, y_predicted)
        loss = total_loss / len(val_dataloader)
        f1 = get_f1(y_true, y_predicted)

        print('Evaluation accuracy: %f' % (acc))
        print('Evaluation loss: %f' % (loss))
        print('Evaluation f1 score: %f' % (f1))

        return acc, loss, f1
