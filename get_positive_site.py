
import os
import shutil
import pandas as pd
import numpy as np

def save_pos_site(result_txt, source_folder, target_folder):
    '''
    Save reported positive sites
    :param result_txt: txt path for phish-discovery results
    :param source_folder: data folder
    :param target_folder: folder to save positive sites
    :return:
    '''
    df = pd.read_table(result_txt, encoding='ISO-8859-1')
    # df_pos = df.loc[df['phish'] == 1]
    df = [x.strip().split('\t') for x in open(result_txt, encoding='ISO-8859-1').readlines()]
    df_pos = [x for x in df if (len(x) >= 3) and (x[2] == '1')]
    print('Number of reported positive: {}'.format(len(df_pos)))

    if len(df_pos) == 0:
        return
    os.makedirs(target_folder, exist_ok=True)
    # for folder in list(df_pos['folder']):
    for folder in [x[0] for x in df_pos]:
        if 'autodiscover' == folder.split('.')[0] or 'outlook' == folder.split('.')[0]: # FIXME: filter out those webmail service
            continue
        try:
            shutil.copytree(os.path.join(source_folder, folder),
                        os.path.join(target_folder, folder))
        except FileExistsError as e:
            print(e)
            continue
        except FileNotFoundError as e:
            print(e)
            continue
        except Exception as e:
            print(e)
            continue

def get_diff(bigger_folder, smaller_folder, target_folder):
    '''
    Get set(bigger_folder) - set(smaller_folder)
    :param bigger_folder:
    :param smaller_folder:
    :param target_folder: folder to save diff sites
    :return:
    '''
    os.makedirs(target_folder, exist_ok=True)
    for folder in os.listdir(bigger_folder):
        if folder not in os.listdir(smaller_folder):
            try:
                shutil.copytree(os.path.join(bigger_folder, folder),
                                os.path.join(target_folder, folder))
            except FileExistsError:
                continue
            except FileNotFoundError:
                continue

def get_runtime(result_txt):
    '''
    Get 5-number summary statistics for runtime
    :param result_txt:
    :return:
    '''
    df = pd.read_table(result_txt, encoding='ISO-8859-1')
    runtime_list = list(df['runtime (layout detector|siamese|crp classifier|login finder total|login finder process)'])
    totaltime_list = list(df['total_runtime'])

    for i, x in enumerate(runtime_list):
        if isinstance(x, float):
            print(i, x)

    breakdown = [list(map(float, x.split('|'))) for x in runtime_list if not isinstance(x, float)]
    breakdown_df = pd.DataFrame(breakdown)
    breakdown_df.columns = ['layout', 'siamese', 'crp', 'dynamic', 'dynamic_partial']
    breakdown_df = breakdown_df.replace(0, np.NaN)
    print('Minimum: \n', breakdown_df.min(), '\n',
          'Median: \n', breakdown_df.median(), '\n',
          'Mean: \n', breakdown_df.mean(), '\n',
          'Maximum: \n', breakdown_df.max(), '\n')

    print('Total time Min|Median|Mean|Max: \n')
    print(np.nanmin(totaltime_list), np.nanmedian(totaltime_list), np.nanmean(totaltime_list), np.nanmax(totaltime_list))


def get_count(date):
    count_pedia = len(os.listdir('./datasets/PhishDiscovery/Phishpedia/{}'.format(date)))
    count_intention = len(os.listdir('./datasets/PhishDiscovery/PhishIntention/{}'.format(date)))

    print('Phishpedia ct', count_pedia)
    print('Phishintention ct', count_intention)


if __name__ == '__main__':
    date = '2021-04-25'
    # for phishpedia
    save_pos_site('./{}_pedia.txt'.format(date), 'Z:\\{}'.format(date), #TODO: move to Y: disk
                  './datasets/PhishDiscovery/Phishpedia/{}'.format(date))
    #
    # # for phishintention
    save_pos_site('./{}.txt'.format(date), 'Z:\\{}'.format(date),
                  './datasets/PhishDiscovery/PhishIntention/{}'.format(date))
    #
    # # for phishpedia
    save_pos_site('./{}_pedia.txt'.format(date), 'E:\\screenshots_rf\\{}'.format(date),
                  './datasets/PhishDiscovery/Phishpedia/{}'.format(date))
    #
    # # for phishintention
    save_pos_site('./{}.txt'.format(date), 'E:\\screenshots_rf\\{}'.format(date),
                  './datasets/PhishDiscovery/PhishIntention/{}'.format(date))
    #
    # # get phishintention - phishpedia
    get_diff(target_folder='./datasets/PhishDiscovery/intention_pedia_diff/{}'.format(date),
             smaller_folder='./datasets/PhishDiscovery/Phishpedia/{}'.format(date), bigger_folder='./datasets/PhishDiscovery/PhishIntention/{}'.format(date))

    get_runtime('./{}.txt'.format(date))

    # get_count(date)