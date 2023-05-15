import pickle
import random
import numpy as np


TRAINER_LEVEL_MAPPER = {
    'beginner': [10, 31],
    'intermidiate': [30, 66],
    'expert': [65, 101],
}

TRAINER_LEVEL_SUM = {
    'beginner': 120,
    'intermidiate': 260,
    'expert': 400
}

GOAL_MAPPER = {
    'fit': 0,
    'lose_weight': -1,
    'gain_weight': 1
}

PREDICTION_MAPPER = {
    'fit': 0, 'gain': 1, 'lose': 2
}


def generate_population(num_individuals, vector_dim, trainer_level):
    population = np.zeros((num_individuals, vector_dim))

    threshold = vector_dim // 2
    lower, upper = TRAINER_LEVEL_MAPPER[trainer_level]
    
    for idx, individual in enumerate(population):
        individual[np.random.choice(np.arange(threshold))] = random.randrange(lower, upper, 5)
        individual[np.random.choice(np.arange(threshold))] = random.randrange(lower, upper, 5)
        individual[-np.random.choice(np.arange(1, threshold))] = random.randrange(lower, upper, 5)
        individual[-np.random.choice(np.arange(1, threshold))] = random.randrange(lower, upper, 5)
        population[idx] = individual
    return population


class Fitness:
    def __init__(self, filename) -> None:
        self.model = pickle.load(open(filename, 'rb'))
        self.class_mapper = {class_pred: idx for idx, class_pred in enumerate(self.model.classes_)}

    def predict(self, X):
        return self.model.predict(X)
    
    def predict_proba(self, X, goal):
        predicted_proba = self.model.predict_proba(X)
        return [prediction[self.class_mapper[goal]] for prediction in predicted_proba]
    
    def softmax(self, proba):
        return proba / np.sum(proba)
    
    def estimate_fitness(self, X, goal):
        # predictions = self.predict(X)
        proba_predictions = self.predict_proba(X, goal)
        normalized_prob = self.softmax(proba_predictions)
        return normalized_prob
    

def random_selection(population, fitness, goal):
    population_probabilities = fitness.estimate_fitness(population, goal)
    selected_idx = np.random.choice(np.arange(population.shape[0]), p=population_probabilities)
    return population[selected_idx]

# def fitness(individual, current_objective):
#     return np.sum(individual) / TRAINER_LEVEL_SUM[current_objective]

def mutate(individual):
    vector_exercise = np.where(individual != 0)

    individual[np.random.choice(vector_exercise[0])] += 10
    return individual

def crossover(x, y):
    lower_limit = np.random.choice(np.arange(7))
    upper_limit = lower_limit + 4

    new_individual = x.copy()
    new_individual[lower_limit: upper_limit] = y[lower_limit: upper_limit]
    # new_y[lower_limit: upper_limit] = x[lower_limit: upper_limit]
    return new_individual

def gna_scheduler(population, goal):

    fitness = Fitness('sklearn-models/random_forest_weights.pkl')
    i = 0
    new_population = []
    while i != 200:
        
        for _ in range(len(population)):
            x = random_selection(population, fitness, goal)
            # y_population = np.array([element for element in population if all(np.equal(element, x))])
            y = random_selection(population, fitness, goal)
            new_individual = crossover(x, y)
            
            if np.random.rand() < 0.2:
                new_individual = mutate(new_individual)
            
            new_population.append(new_individual)
        i += 1
    return new_population


def select_best_schedule(data, goal):
    model = pickle.load(open('sklearn-models/random_forest_weights.pkl', 'rb'))
    indexes = np.where(model.predict(data) == 'lose')

    probability_list = []

    for index in indexes[0]:
        predicted_proba = model.predict_proba([data[index]])
        probability_list.append(predicted_proba[0][PREDICTION_MAPPER[goal]])
    
    index_max_value_probability = probability_list.index(max(probability_list))
    
    selected_schedule_index = indexes[0][index_max_value_probability]
    selected_schedule = data[selected_schedule_index]
    return selected_schedule
# new_population = gna_scheduler(generate_population(10, 10, 'intermidiate'), 'lose')