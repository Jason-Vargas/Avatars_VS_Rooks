// ----------------------------------------------------
// PasswordToggle.cs
// Manejar la lógica del boton que esconde la contraseña
// Autor: Iván Ignacio Brito Medina
// ----------------------------------------------------
using TMPro;
using UnityEngine;

public class PasswordToggle : MonoBehaviour
{
    [Header("Campos de contraseña a afectar:")]
    [SerializeField] private TMP_InputField[] passwordFields;

    [Header("Texto del icono (Unicode):")]
    [SerializeField] private TMP_Text eyeIconText;

    [Tooltip("Carácter Unicode cuando la contraseña está oculta (por ejemplo: 👁️, 🔒, 🕶️)")]
    [SerializeField] private string hideChar = "👁️";
    [Tooltip("Carácter Unicode cuando la contraseña está visible (por ejemplo: 🚫, ❌, 🔓)")]
    [SerializeField] private string showChar = "🚫";

    private bool isPasswordVisible = false;

    public void TogglePasswordVisibility()
    {
        isPasswordVisible = !isPasswordVisible;

        // Alternar tipo de contenido en todos los campos
        foreach (TMP_InputField field in passwordFields)
        {
            if (field == null) continue;

            field.contentType = isPasswordVisible
                ? TMP_InputField.ContentType.Standard
                : TMP_InputField.ContentType.Password;

            field.ForceLabelUpdate();
        }

        // Cambiar el carácter Unicode del icono
        if (eyeIconText != null)
        {
            eyeIconText.text = isPasswordVisible ? showChar : hideChar;
        }
    }
}
