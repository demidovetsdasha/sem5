package org.example.testomis.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.ToString;
import org.example.testomis.model.enums.EventCategory;

import java.util.Date;
import java.util.List;

@Data
@Entity
public class Event {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Long id;

    private String name;

    private EventCategory category;

    private String author;

    @ManyToOne(cascade = CascadeType.PERSIST, fetch = FetchType.LAZY)
    @ToString.Exclude
    private User user;

    private Date start;

    private Date finish;

    @OneToOne(cascade = CascadeType.PERSIST, fetch = FetchType.LAZY)
    private PresentationData file;
}
