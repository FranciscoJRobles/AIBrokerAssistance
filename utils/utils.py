def json_clean_response(data: str) -> str:
    """
    Limpia una cadena eliminando caracteres específicos que puedan estar fuera del JSON.

    Args:
        data: Cadena con los datos a limpiar.

    Returns:
        Cadena limpia.
    """
    if isinstance(data, str):
        # Eliminar caracteres específicos como ```json y ``` fuera del JSON
        data = data.replace('```json', '').replace('```', '').replace('\n', '').strip()
    return data