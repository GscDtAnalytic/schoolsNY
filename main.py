import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Carrega o CSV
    schools = pd.read_csv('schools.csv')

    # Exibe um preview legível no terminal
    print(schools.to_string(index=False))

    # Seleciona colunas (ajuste `school_name` se seu CSV usar `schoo_name`)
    best_math_schools = schools[schools['average_math'] >= 640][['school_name', 'average_math']].sort_values(by='average_math', ascending=False)

    print(best_math_schools.to_string(index=False))

    # Calcula a soma das médias de SAT

    schools['total_SAT'] = schools[['average_math', 'average_reading', 'average_writing']].sum(axis=1,numeric_only=True)
    top_10_schools = schools[['school_name','total_SAT']].sort_values(by='total_SAT', ascending=False).head(10)

    print(top_10_schools.to_string(index=False))

    # Agrupa por borough e calcula a média e o desvio padrão
    stats_borough = schools.groupby('borough').agg({
        'school_name': 'count',  # para contar o número de escolas
        'total_SAT': ['mean', 'std']  # para calcular média e desvio padrão
    }).reset_index()


    stats_borough.columns = ['borough', 'num_schools', 'average_SAT', 'std_SAT']
    largest_std_dev = stats_borough\
    .sort_values(by='std_SAT', ascending=False)\
    .head(1)\
    .set_index('borough')\
    [['num_schools', 'average_SAT', 'std_SAT']]\
    .round(2)
    print(largest_std_dev)

    # 1) Histograma de total_SAT
    plt.figure(figsize=(8, 5))
    plt.hist(schools['total_SAT'].dropna(), bins=30, color='C0', edgecolor='k', alpha=0.8)
    plt.title('Distribuição de total_SAT')
    plt.xlabel('total_SAT')
    plt.ylabel('Número de escolas')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('hist_total_SAT.png')
    plt.show()

    # 2) Boxplot por borough
    if 'borough' in schools.columns:
        data = [grp['total_SAT'].dropna().values for _, grp in schools.groupby('borough')]
        labels = [str(b) for b, _ in schools.groupby('borough')]
        plt.figure(figsize=(10, 6))
        # chama sem o argumento de rótulos para evitar a deprecação
        plt.boxplot(data, patch_artist=True)
        # define os rótulos manualmente nas posições 1..N
        plt.xticks(range(1, len(labels) + 1), labels, rotation=45)
        plt.title('Boxplot de total_SAT por borough')
        plt.xlabel('Borough')
        plt.ylabel('total_SAT')
        plt.tight_layout()
        plt.savefig('boxplot_by_borough.png')
        plt.show()

    # 3) Top 10 escolas por total_SAT
    plt.figure(figsize=(10, 6))
    plt.barh(top_10_schools['school_name'][::-1], top_10_schools['total_SAT'][::-1], color='C1')
    plt.title('Top 10 escolas por total_SAT')
    plt.xlabel('total_SAT')
    plt.tight_layout()
    plt.savefig('top10_schools.png')
    plt.show()

    # 4) Scatter math x reading colorido por borough
    if 'average_math' in schools.columns and 'average_reading' in schools.columns:
        plt.figure(figsize=(8, 6))
        if 'borough' in schools.columns:
            for b, grp in schools.groupby('borough'):
                plt.scatter(grp['average_math'], grp['average_reading'], label=str(b), alpha=0.7, s=40)
            plt.legend(title='borough', bbox_to_anchor=(1.05, 1), loc='upper left')  # correção: 'upper left'
        else:
            plt.scatter(schools['average_math'], schools['average_reading'], alpha=0.7, s=40)
        plt.title('average_math vs average_reading')
        plt.xlabel('average_math')
        plt.ylabel('average_reading')
        plt.tight_layout()
        plt.savefig('scatter_math_reading.png')
        plt.show()

    # 5) Média e desvio padrão por borough
    if 'borough' in schools.columns:
        stats = schools.groupby('borough')['total_SAT'].agg(['mean', 'std', 'count']).dropna()
        plt.figure(figsize=(10, 6))
        x = np.arange(len(stats))
        plt.bar(x, stats['mean'], yerr=stats['std'], capsize=5, color='C2', alpha=0.9)
        plt.xticks(x, stats.index, rotation=45)
        plt.ylabel('Média total_SAT (erro = std)')
        plt.title('Média e desvio padrão de total_SAT por borough')
        plt.tight_layout()
        plt.savefig('mean_std_by_borough.png')
        plt.show()

        # 6) Contagem de escolas por borough
        plt.figure(figsize=(8, 5))
        stats['count'].sort_values(ascending=False).plot(kind='bar', color='C3')
        plt.title('Número de escolas por borough')
        plt.xlabel('Borough')
        plt.ylabel('Número de escolas')
        plt.tight_layout()
        plt.savefig('count_by_borough.png')
        plt.show()


if __name__ == '__main__':
    main()
