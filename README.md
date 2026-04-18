{% extends 'base.html' %}
{% block content %}
<div class="form-card card narrow">
    <h1>Create Event</h1>
    <form method="post" class="form-grid">
        <label>Title<input type="text" name="title" required /></label>
        <label>Type
            <select name="event_type">
                <option value="game">Game</option>
                <option value="practice">Practice</option>
                <option value="tournament">Tournament</option>
                <option value="meeting">Meeting</option>
            </select>
        </label>
        <label>Team
            <select name="team_id">
                {% for team in teams %}
                    <option value="{{ team.id }}">{{ team.name }}</option>
                {% endfor %}
            </select>
        </label>
        <label>Start time<input type="datetime-local" name="start_time" required /></label>
        <label>End time<input type="datetime-local" name="end_time" required /></label>
        <label>Location<input type="text" name="location" /></label>
        <label>Notes<textarea name="notes" rows="4"></textarea></label>
        <button class="button" type="submit">Save Event</button>
    </form>
</div>
{% endblock %}
