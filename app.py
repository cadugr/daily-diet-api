from flask import Flask, request, jsonify
from datetime import datetime

# Importações locais
from database import db
from models.user import User
from models.meal import Meal

app = Flask(__name__)

# Configuração do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet-db'

# Inicializa o banco
db.init_app(app)

# ---------------------------
# Rotas Usuários
# ---------------------------
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(name=data["name"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "name": user.name}), 201


@app.route("/users", methods=["GET"])
def list_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name} for u in users])

# ---------------------------
# Rotas Refeições
# ---------------------------
@app.route("/meals", methods=["POST"])
def create_meal():
    data = request.json
    user = User.query.get(data["user_id"])

    if user:
        meal = Meal(
            name=data["name"],
            description=data["description"],
            meal_date=datetime.fromisoformat(data["meal_date"]),
            is_on_diet=data["is_on_diet"],
            user_id=data["user_id"]
        )
        db.session.add(meal)
        db.session.commit()
        return jsonify({"message": f"Refeição cadastrada com código {meal.id}"}), 201
    
    return jsonify({"message": f"Não é possível cadastrar a refeição para o usuário de id {data["user_id"]}, pois o mesmo não existe cadastrado no sistema."}), 400

@app.route("/meals/<int:meal_id>", methods=["GET"])
def get_meal(meal_id):
    meal = Meal.query.get(meal_id)

    if meal:
        return jsonify({
            "id": meal.id,
            "name": meal.name,
            "description": meal.description,
            "meal_date": meal.meal_date.isoformat(),
            "is_on_diet": meal.is_on_diet,
            "user_id": meal.user_id
        })
    return jsonify({"message": f"Refeição não encontrada com o código {meal_id}."}), 404

@app.route("/users/<int:user_id>/meals", methods=["GET"])
def list_meals(user_id):
    user = User.query.get(user_id)

    if user:
        meals = Meal.query.filter_by(user_id=user.id).all()
        return jsonify([
            {
                "id": m.id,
                "name": m.name,
                "description": m.description,
                "meal_date": m.meal_date.isoformat(),
                "is_on_diet": m.is_on_diet,
                "user_id": m.user_id
            } for m in meals
        ])
    
    return jsonify({"message": f"Não foi possível recuperar refeições para o usuário de id {user_id}, pois o mesmo não existe no sistema."}), 404


@app.route("/meals/<int:meal_id>", methods=["PUT"])
def update_meal(meal_id):
    data = request.json
    meal = Meal.query.get(meal_id)

    if meal:
        meal.name = data.get("name")
        meal.description = data.get("description")
        if "meal_date" in data:
            meal.meal_date = datetime.fromisoformat(data["meal_date"])
        if "is_on_diet" in data:
            meal.is_on_diet = data["is_on_diet"]

        db.session.commit()
        return jsonify({"message": f"Refeição de código {meal_id} atualizada com sucesso"})
    
    return jsonify({"message": f"Não foi possível atualizar a refeição de código {meal_id}, pois a mesma não existe no sistema."}), 404

@app.route("/meals/<int:meal_id>", methods=["DELETE"])
def delete_meal(meal_id):
    meal = Meal.query.get(meal_id)

    if meal:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": "Refeição removida com sucesso"})
    
    return jsonify({"message": f"Não foi possível remover a refeição de código {meal_id}, pois a mesma não existe no sistema."}), 404



# ---------------------------
# Inicialização
# ---------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.run(debug=True)