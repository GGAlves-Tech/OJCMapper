# Avaliação do Pitch: Projeto MAPPER

## 📄 Texto Extraído (O "Pitch" do Projeto)

> "O gerenciamento eficaz de unidades de rede é um aspecto crucial na otimização de processos de produção [...]. Pensando nessa necessidade, a Rede Anhanguera, mantida pela empresa Centro Norte de Comunicação Ltda, com sede em Palmas-TO, busca soluções que modernizem os fluxos de trabalho de produção audiovisual. O projeto MAPPER visa desenvolver um software que possibilite o mapeamento intuitivo de pastas em um ambiente de rede compartilhado, permitindo que as ilhas de edição tenham acesso a um repositório que mesmo centralizado permita o acesso a todos os vídeos [...]
>
> Este documento é baseado em estatísticas colhidas durante estudos realizados com objetivos específicos de implantar um novo fluxo de edição na emissora de Palmas. Com os levantamentos chegou-se a conclusão do uso médio de 4TB por semana de dados do jornalismo, sendo 12TB por mês. Destes dados, verificou-se que 92% são mídias provenientes de “ingest” [...] e 8% são as mídias de arquivo (CEDOC). 
> 
> Baseado nisso, a proposta deste projeto além de inserir um workflow para rotina da captura ao arquivamento deve inserir uma nova ferramenta para que seja possível melhorar a forma dos editores terem acesso aos projetos que estão armazenados no Storage. Idealizando um ecossistema que permita uma edição compartilhada e centralizada [...] A implementação do MAPPER não apenas atenderá a essa necessidade, mas também proporcionará um ambiente mais coeso para a equipe de edição, permitindo que os projetos sejam compartilhados de maneira organizada e simplificada."

---

## 👨‍🏫 Avaliação do "Professor"

**Prezados alunos (Adriano, Diana, Guthemberg e Kauãn),**

Analisando a justificativa e o escopo apresentados para o **Mapper OJC**, devo parabenizar a equipe pela excelência na concepção e pelo claro alinhamento com as necessidades do mercado. Um bom Projeto Integrador precisa resolver a dor real de um cliente real, e vocês conseguiram capturar isso com maestria.

Abaixo, apresento minhas considerações divididas em eixos de avaliação:

### 🟢 1. Apresentação do Problema e Embalsamento em Dados (Excelente)
O ponto altíssimo do texto de vocês é a quantificação do problema. Em pitches empresariais ou acadêmicos, dizer "temos muito arquivo" é vago; mas dizer *"produzimos 4TB por semana de dados de jornalismo, sendo 92% de ingest bruto e 8% do CEDOC"* demonstra pesquisa impecável na fase de Requisitos. Vocês provaram que não deduziram o problema, vocês **mediram** o problema no ambiente real da Rede Anhanguera. 

### 🟢 2. Integração com Ecossistema Enterprise (Muito Bom)
Gostei bastante de como o texto contextualiza a ferramenta não como um software isolado, mas como uma peça de um quebra-cabeça corporativo altamente complexo e caro (Storage local Quantum Stornext 5, AVID Media Composer e NewsCutter). Isso aumenta o valor percebido da solução de vocês. O software será o "cimento" entre o hardware de storage e as ferramentas de ponta de edição.

### 🟡 3. Clareza do "Pitch" Comercial (Ponto de Atenção)
Enquanto documentação técnica e introdução de TCC, a redação está impecável e madura. No entanto, se formos avaliar estritamente como um **Pitch** (aquela defesa de 3 minutos para convencer um gestor a investir no seu sistema), a estrutura pode ser invertida para ficar mais "matadora".
* **Atualmente:** Vocês começam com abstrações técnicas (*"O gerenciamento eficaz de redes é crucial..."*) e vão para o problema real só no segundo tópico.
* **Como melhorar (Formato Pitch):** Comecem com a dor (a "faca no pescoço" do cliente) e terminem com o curativo (o software). 

*Exemplo de "Elevator Pitch":*
> *"Hoje, o jornalismo da TV Anhanguera de Palmas gera 12 Terabytes de dados mensais. Com esse volume massivo, a organização manual nas ilhas de edição AVID não é mais sustentável humana ou financeiramente, resultando em perda de tempo crítico na caça de arquivos. Para resolver isso, criamos o MAPPER: uma solução que automatiza o mapeamento dessas unidades de rede no Storage Quantum, garantindo que o editor não perca nem um segundo de produtividade tentando achar onde o vídeo está salvo."*

### 🟢 4. Proposta de Valor e Retorno (Muito Bom)
O texto deixa claro que o ROI (Retorno sobre Investimento) da ferramenta não é necessariamente financeiro direto, mas ganho de produtividade ("facilite a gestão", "evitando assim perda de dados"). Para o contexto de redações jornalísticas onde o tempo é crucial (um furo de reportagem pode atrasar por arquivo mal mapeado), isso é um argumento de venda fortíssimo.

---

### 📝 Veredito
**Nota: 9.5 / 10**

É um projeto robusto, com requisitos levantados de forma séria. O texto comprova a viabilidade e justifica plenamente o esforço de engenharia de software da equipe. Se precisarem apresentar isso para a diretoria de tecnologia, recomendo apenas enxugar a introdução acadêmica, destacando primeiro os números de tráfego de dados e, em seguida, a solução. Estão no caminho certo!
