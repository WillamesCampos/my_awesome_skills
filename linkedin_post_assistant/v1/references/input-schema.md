# Entrada por sessão

Aceite texto livre quando ele trouxer evidência suficiente. Quando faltarem dados, peça somente
os campos relevantes deste modelo:

```yaml
date: YYYY-MM-DD
topic: ""
concepts_studied: []
answers_or_artifacts: []
feedback_received: []
case_type: "simulated | personal_experiment | authorized_real_experience"
demonstrated_points: []
learning_gaps: []
verified_corrections: []
verified_quantitative_results: []
do_not_disclose: []
suggested_angle: ""
editorial_state: "exploratory | ready_for_review | approved"
```

`verified_quantitative_results` deve incluir método, ambiente e origem dos números. Campo vazio
significa que a publicação não pode alegar melhoria quantitativa. `do_not_disclose` tem
prioridade sobre qualquer sugestão de narrativa.
