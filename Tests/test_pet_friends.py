from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


# test 1
def test_add_new_pet_without_photo_valid_data(name='Шерлок', animal_type='Лабрадор', age='2'):
    """Проверяем метод добавления питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем статус и результат
    assert status == 200
    assert result['name'] == name


# test 2
def test_successful_add_pets_correct_photo(pet_photo='images/Sherloc.jpg'):
    """Проверяем, что можно добавить фото питомцу с корректным файлом изображения"""
    # Получаем полный путь к файлу с изображением питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pets_photo(auth_key, pet_photo, my_pets['pets'][0]['id'])

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['pet_photo'] != ''
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception('Список питомцев пуст')


# test 3
def test_get_api_key_for_invalid_user(email='name@mail.com', password='password'):
    """Проверяем что запрос api ключа для незарегистрированного пользователя возвращает статус 403"""
    status, _ = pf.get_api_key(email, password)
    assert status == 403


# test 4
def test_get_all_pets_with_invalid_key(filter=''):
    """Проверяем что запрос всех питомцев с некорректным api ключом возвращает код 403"""
    auth_key = {
        'key': 'really-incorrect-api-key'
    }
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403


# test 5
def test_add_new_pet_without_photo_negative_age(name='Соня', animal_type='кошка', age='-3'):
    """Проверяем возможность добавления питомца с отрицательным возрастом. Ожидается код 400"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем статус
    assert status == 400


# test 6
def test_add_new_pet_without_photo_empty_name(name='', animal_type='', age=''):
    """Проверяем возможноть добавить питомца с пустыми значениями"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем статус
    assert status != 200


# test 7
def test_add_new_pet_with_valid_data(name='$+@%*&', animal_type='//-#^))', age='?'):
    """Проверяем возможность добавить питомца с некорректными данными (в виде символов)"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем статус
    assert status != 200


# test 8
def test_post_api_create_pet_simple_unauthorized_user(name='Zevs', animal_type='кот', age='5'):
    """Проверяем возможность добавить питомца неавторизованным пользователем"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key('', '')

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# test 9
def test_delete_api_first_pet():
    """Проверяем возможность удаления первого добавленного питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    print(my_pets)

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Alex", "кот", "4")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        print(my_pets)

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][-1]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")


    # Проверяем, что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


# test 10
def test_put_api_pet_no_name(name='', animal_type='кошка', age=3):
    """Проверяем возможность обновления информации о питомце без указания его имени"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if name == '':
        raise Exception('Не указано имя питомца')
    elif len(my_pets['pets']) > 0:
        status, result = pf.put_api_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age,
                                        pet_photo='images/Sonya.jpg')

        # Проверяем, что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Питомцев нет")


# test 11
def test_add_invalid_photo_of_pet(pet_photo='images/monkey.txt'):
    """Проверяем возможность добавления текстового файла вместо фото питомца"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pets_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа != 200 и фото питомца не появилось
        assert status != 200
        assert result['pet_photo'] != ''
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
