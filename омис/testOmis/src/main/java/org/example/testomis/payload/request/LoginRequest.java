package org.example.testomis.payload.request;

import jakarta.validation.constraints.NotEmpty;
import lombok.Data;

@Data
public class LoginRequest {
    @NotEmpty(message = "email cant be empty")
    private String username;
    @NotEmpty(message = "password cant be empty")
    private String password;
}
