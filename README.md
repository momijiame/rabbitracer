rabbitracer
===========


# ����͉��H

RabbitMQ �ɗ����S�Ẵ��b�Z�[�W�� JSON �Ń_���v���邽�߂̃X�N���v�g�ł��B
RabbitMQ ���p�����V�X�e���̃f�o�b�O�ɗL�p�ł��B

# �C���X�g�[��

�C���X�g�[���Ǝ��s�ɂ� Python ���K�v�ł��B

```
$ git clone https://github.com/momijiame/rabbitracer.git
$ cd rabbitracer
$ python setup.py install
```

# �g����

RabbitMQ ���N��������Ԃ� Firehose �@�\��L���ɂ��܂��B

```
$ rabbitmqctl stop_app
$ rabbitmqctl trace_on
$ rabbitmqctl start_app
```

�X�N���v�g�����s����� RabbitMQ �ɗ���郁�b�Z�[�W�� JSON �ŏo�͂���܂��B
�f�t�H���g�ł̓��[�J���z�X�g�ɃQ�X�g�A�J�E���g�Őڑ����܂��B
�ύX����ꍇ�̓I�v�V�����Ŏw��ł��܂��B

```
$ rabbitracer
```
