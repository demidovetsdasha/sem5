package org.example.testomis.payload;

import jakarta.validation.constraints.NotEmpty;
import lombok.Data;

@Data
public class UserDTO {

    private Long id;
    @NotEmpty
    private String firstname;
    @NotEmpty
    private String lastname;

    @NotEmpty
    private String username;

    private String bio;

}
