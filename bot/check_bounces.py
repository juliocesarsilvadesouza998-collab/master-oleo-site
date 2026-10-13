import csv

problematic_emails = {'rh@realgastronomia.com.br', 'faleconosco@beirariosm.com.br', 'comunicacao@bionatusfarma.com.br', 'avesideal@rosaves.com.br', 'contato@kerry.com', 'contato@pedrinhoatacadista.com.br', 'contato@deltaterceirizacoes.com.br', 'contato@scallet.com.br', 'nutraway@nutraway.com.br', 'contato@arcor.com', 'ecommerce704@redetop.com.b', 'sac@redeoba.com.br', 'ana@alimentossalto.com.br', 'info@kelcopetcare.com.br', 'sac@oba.com.br', '3d@roldao.com.br', 'contato@hrtcosmeticos.com.br', 'contato@eixorestaurantes.co', 'contato@nutraway.com.br', 'ecommerce704@redetop.com.br', 'contato@arese.com.br', 'contato@selmi.com.br'}

with open('leads.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['email'] in problematic_emails:
            print(f"{row['email']}: status={row['status']}, criado_em={row['criado_em'][:10]}")