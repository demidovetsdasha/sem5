package org.example.testomis.payload.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;
import lombok.Data;
import org.example.testomis.annotations.PasswordMatches;
import org.example.testomis.annotations.ValidEmail;

@Data
@PasswordMatches
public class SignupRequest {
    @Email(message = "it should be email format")
    @NotBlank(message = "User email is required")
    @ValidEmail
    private String email;
    @NotEmpty(message = "enter your name")
    private String firstname;
    @NotEmpty(message = "enter your lastname")
    private String lastname;
    @NotEmpty(message = "enter your username")
    private String username;
    @NotEmpty(message = "password is required")
    @Size(min = 8)
    private String password;
    private String confirmPassword;
}
