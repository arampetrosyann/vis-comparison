# Visualization Systems Comparison

To setup and run:

1. ```bash setup_env.sh <tool-name>```
2. ```bash run.sh <tool-name>```

## Notes

### Table2Charts
The system mainly provides the model plus training and inference scripts. Inference returns ranked chart recommendations (fields and chart types) in a specific format. Additional work is needed to convert raw CSV data into the required model input format and then map recommendations into actual visualization specifications and plots.

### KG4Vis 
The implementation contains the model and training scripts only. The results obtained after training is [here](./experiments/kg4vis/rules.csv). The system is partially implemented.
