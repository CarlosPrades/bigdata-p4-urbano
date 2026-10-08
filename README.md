# Proyecto 4 ·  Big Data urbano (Valencia)


## Descripción y objetivo

Pipeline completo de ingeniería de datos (batch + streaming) sobre datos abiertos de tráfico, calidad del aire y meteorología de Valencia. Los datos se cruzan con Spark y el proyecto termina con dos modelos predictivos: uno principal de NO₂ horario y uno secundario de intensidad de tráfico.

## Arquitectura

```mermaid
graph LR
    A[Entidades meteorológicas] --> B[Ingesta]
    B --> C[Data Lake + MongoDB]
    C --> D[Spark (batch)]
    D --> E[IA aplicada]
```