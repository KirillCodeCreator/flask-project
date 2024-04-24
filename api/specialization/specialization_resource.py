from flask import jsonify
from flask_restful import Resource, abort, Api

from api.specialization.reqparse_specialization import parser
from data import db_session
from data.specialization import Specialization


# выкидываем ответ 404 на запрос когда не найдена специализация врача с заданным specialization_id
def abort_missing_specialization(specialization_id):
    db_sess = db_session.create_session()
    specialization = db_sess.get(Specialization, specialization_id)
    if not specialization:
        abort(404, message=f"Специализация врача с id = {specialization_id} не найдена")


# описываем методы для доступа к конкретной специализации врачей
class SpecializationResource(Resource):
    def get(self, specialization_id):
        abort_missing_specialization(specialization_id)
        db_sess = db_session.create_session()
        specialization = db_sess.query(Specialization).get(specialization_id)
        return jsonify(
            {"specializations": [specialization.to_dict()]}
        )

    def put(self, specialization_id):
        abort_missing_specialization(specialization_id)
        args = parser.parse_args()
        db_sess = db_session.create_session()
        specialization = db_sess.get(Specialization, specialization_id)
        specialization.title = args["title"]
        db_sess.commit()
        return jsonify({'success': 'OK', 'message': 'Специальность успешно обновлена'})

    def delete(self, specialization_id):
        abort_missing_specialization(specialization_id)
        db_sess = db_session.create_session()
        specialization = db_sess.get(Specialization, specialization_id)
        db_sess.delete(specialization)
        db_sess.commit()
        return jsonify({'success': 'OK', 'message': f'Специальность "{specialization.title}" успешно удалена'})


# описываем методы для доступа к списку специализаций врачей
class SpecializationsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        specializations = db_sess.query(Specialization).all()
        return jsonify(
            {"specializations": [specialization.to_dict() for specialization in specializations]}
        )

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        specialization = Specialization(
            title=args["title"])
        db_sess.add(specialization)
        db_sess.commit()
        return jsonify(
            {
                'Success': 'OK',
                'id': specialization.id,
                'message': f'Специальность "{specialization.title}" успешно добавлена'
            })


def add_api_specializations_routes(api: Api):
    url_prefix = "/api/specializations"
    api.add_resource(SpecializationResource, f"{url_prefix}/<int:specialization_id>")
    api.add_resource(SpecializationsListResource, url_prefix)
