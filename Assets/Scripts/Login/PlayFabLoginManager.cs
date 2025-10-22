// ----------------------------------------------------
// PlayFabLoginManager.cs
// Login y registro PlayFab con botones separados para cambiar panel
// Autor: Iván Ignacio Brito Medina
// ----------------------------------------------------
using TMPro;
using UnityEngine;
using PlayFab;
using PlayFab.ClientModels;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
public class PlayFabLoginManager : MonoBehaviour
{
    [Header("Paneles de la UI")]
    [SerializeField] private GameObject loginPanel;
    [SerializeField] private GameObject registerPanel;

    [Header("Login UI")]
    [SerializeField] private TMP_InputField loginUsername;
    [SerializeField] private TMP_InputField loginPassword;
    [SerializeField] private Button loginButton;     // Acción real de login
    [SerializeField] private Button goToRegister;    // Cambiar a panel registro

    [Header("Register UI")]
    [SerializeField] private TMP_InputField registerEmail;
    [SerializeField] private TMP_InputField registerUsername;
    [SerializeField] private TMP_InputField registerPassword;
    [SerializeField] private Button registerButton;  // Acción real de registro
    [SerializeField] private Button goToLogin;       // Cambiar a panel login

    [Header("Texto de error")]
    [SerializeField] private TMP_Text textError;

    private bool showingLogin = true;

    private void Start()
    {
        ShowLoginPanel();

        loginButton.onClick.AddListener(OnLoginPressed);
        registerButton.onClick.AddListener(OnRegisterPressed);
        goToRegister.onClick.AddListener(ShowRegisterPanel);
        goToLogin.onClick.AddListener(ShowLoginPanel);
    }

    private void Update()
    {
        loginButton.interactable = showingLogin ? AreLoginFieldsFilled() : true;

        registerButton.interactable = !showingLogin ? AreRegisterFieldsFilled() : true;

        goToLogin.interactable = true;
        goToRegister.interactable = true;
    }

    private bool AreLoginFieldsFilled()
    {
        return !string.IsNullOrEmpty(loginUsername.text)
            && !string.IsNullOrEmpty(loginPassword.text);
    }

    public void OnLoginPressed()
    {
        if (AreLoginFieldsFilled())
        {
            Login(loginUsername.text, loginPassword.text);
        }
    }

    private void Login(string username, string password)
    {
        var request = new LoginWithPlayFabRequest
        {
            Username = username,
            Password = password,
            InfoRequestParameters = new GetPlayerCombinedInfoRequestParams
            {
                GetPlayerProfile = true
            }
        };

        PlayFabClientAPI.LoginWithPlayFab(
            request,
            result =>
            {
                Debug.Log("✅ Login exitoso: " + result.PlayFabId);
                SceneManager.LoadSceneAsync("Menu");
            },
            error =>
            {
                ShowError("Error al iniciar sesión: " + error.ErrorMessage);
                Debug.LogError("❌ Error login: " + error.GenerateErrorReport());
            }
        );
    }

    private bool AreRegisterFieldsFilled()
    {
        return !string.IsNullOrEmpty(registerEmail.text)
            && !string.IsNullOrEmpty(registerUsername.text)
            && !string.IsNullOrEmpty(registerPassword.text);
    }

    public void OnRegisterPressed()
    {
        if (AreRegisterFieldsFilled())
        {
            Register(registerEmail.text, registerUsername.text, registerPassword.text);
        }
    }

    private void Register(string email, string username, string password)
    {
        PlayFabClientAPI.RegisterPlayFabUser(new RegisterPlayFabUserRequest
        {
            Email = email,
            Username = username,
            Password = password,
            RequireBothUsernameAndEmail = true
        },
        successResult =>
        {
            Login(username, password);
        },
        error =>
        {
            ShowError("❌ Error al registrar: " + error.ErrorMessage);
            Debug.LogError("❌ PlayFab Error: " + error.GenerateErrorReport());
        });
    }


    public void ShowLoginPanel()
    {
        showingLogin = true;
        loginPanel.SetActive(true);
        registerPanel.SetActive(false);
        Debug.Log("🔹 Mostrando panel Login");
    }

    public void ShowRegisterPanel()
    {
        showingLogin = false;
        loginPanel.SetActive(false);
        registerPanel.SetActive(true);
        Debug.Log("🔹 Mostrando panel Registro");
    }

    private void ShowError(string message)
    {
        if (textError != null)
            textError.text = message;
    }

    private void ClearError()
    {
        if (textError != null)
            textError.text = "";
    }
}
