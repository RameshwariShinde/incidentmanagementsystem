from flask import Blueprint, request, jsonify
from app import db, mail
from app.models import Incident
from flask_mail import Message

main = Blueprint('main', __name__)

# Create Incident
@main.route('/incident', methods=['POST'])
def create_incident():
    data = request.get_json()
    new_incident = Incident(title=data['title'], description=data['description'])
    db.session.add(new_incident)
    db.session.commit()

    send_email('New Incident Created', f"Title: {data['title']}\nDescription: {data['description']}")
    return jsonify({'message': 'Incident created'}), 201

# Update Incident
@main.route('/incident/<int:id>', methods=['PUT'])
def update_incident(id):
    incident = Incident.query.get_or_404(id)
    data = request.get_json()

    incident.title = data.get('title', incident.title)
    incident.description = data.get('description', incident.description)
    db.session.commit()
    return jsonify({'message': 'Incident updated'})

# Assign Incident
@main.route('/incident/<int:id>/assign', methods=['PUT'])
def assign_incident(id):
    incident = Incident.query.get_or_404(id)
    data = request.get_json()

    incident.assignee = data['assignee']
    incident.status = 'Assigned'
    db.session.commit()
    return jsonify({'message': 'Incident assigned'})

# Resolve Incident
@main.route('/incident/<int:id>/resolve', methods=['PUT'])
def resolve_incident(id):
    incident = Incident.query.get_or_404(id)
    incident.status = 'Resolved'
    db.session.commit()
    return jsonify({'message': 'Incident resolved'})

# Get All Incidents
@main.route('/incidents', methods=['GET'])
def get_incidents():
    incidents = Incident.query.all()
    return jsonify([{
        'id': i.id,
        'title': i.title,
        'description': i.description,
        'status': i.status,
        'assignee': i.assignee,
        'created_at': i.created_at,
        'updated_at': i.updated_at
    } for i in incidents])

# Email Notification
def send_email(subject, body):
    msg = Message(subject, sender='your_email@gmail.com', recipients=['recipient_email@gmail.com'])
    msg.body = body
    mail.send(msg)
