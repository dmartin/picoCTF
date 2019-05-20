"""Tests for the /api/v1/stats endpoints."""

from common import ( # noqa (fixture)
  ADMIN_DEMOGRAPHICS,
  clear_db,
  client,
  decode_response,
  get_csrf_token,
  register_test_accounts,
  TEACHER_DEMOGRAPHICS,
  USER_DEMOGRAPHICS,
  USER_2_DEMOGRAPHICS,
  load_sample_problems,
  get_conn,
  ensure_within_competition,
  enable_sample_problems,
  get_problem_key
)
import api

def test_registration_stats(client):
    """Test the /stats/registration endpoint."""
    clear_db()
    register_test_accounts()

    # Get the initial registration count
    res = client.get('/api/v1/stats/registration')
    assert res.status_code == 200
    assert res.json == {
        'groups': 0,
        'teamed_users': 0,
        'teams': 0,
        'users': 4
    }

    # Try adding a new user
    res = client.post('/api/v1/users', json={
        'email': 'user3@sample.com',
        'firstname': 'Third',
        'lastname': 'Testuser',
        'password': 'testuser3',
        'username': 'testuser3',
        'affiliation': 'Testing',
        'usertype': 'other',
        'country': 'US',
        'demo': {
            'age': '18+'
        }
    })
    assert res.status_code == 201
    res = client.get('/api/v1/stats/registration')
    assert res.status_code == 200
    assert res.json == {
        'groups': 0,
        'teamed_users': 0,
        'teams': 0,
        'users': 5
    }

    # Have a user create a team
    client.post('api/v1/user/login', json={
        'username': USER_DEMOGRAPHICS['username'],
        'password': USER_DEMOGRAPHICS['password']
    })
    res = client.post('/api/v1/teams', json={
        'team_name': 'newteam',
        'team_password': 'newteam'
    })
    assert res.status_code == 201

    res = client.get('/api/v1/stats/registration')
    assert res.status_code == 200
    assert res.json == {
        'groups': 0,
        'teamed_users': 1,
        'teams': 1,
        'users': 5
    }

    # Have another user join that team
    api.config.get_settings()
    db = get_conn()
    db.settings.find_one_and_update({}, {'$set': {'max_team_size': 2}})
    client.get('/api/v1/user/logout')
    client.post('/api/v1/user/login', json={
        'username': USER_2_DEMOGRAPHICS['username'],
        'password': USER_2_DEMOGRAPHICS['password']
    })
    res = client.post('/api/v1/team/join', json={
        'team_name': 'newteam',
        'team_password': 'newteam'
    })
    assert res.status_code == 200

    res = client.get('/api/v1/stats/registration')
    assert res.status_code == 200
    assert res.json == {
        'groups': 0,
        'teamed_users': 2,
        'teams': 1,
        'users': 5
    }

    # Create a group
    client.get('/api/v1/user/logout')
    client.post('/api/v1/user/login', json={
        'username': TEACHER_DEMOGRAPHICS['username'],
        'password': TEACHER_DEMOGRAPHICS['password']
    })
    res = client.post('/api/v1/groups', json={
        'name': 'newgroup'
    })
    assert res.status_code == 201

    res = client.get('/api/v1/stats/registration')
    assert res.status_code == 200
    assert res.json == {
        'groups': 1,
        'teamed_users': 2,
        'teams': 1,
        'users': 5
    }